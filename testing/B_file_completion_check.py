from _04_mongodb_files import get_attachments
from _02_downloads import get_downloads
import pandas as pd
import requests
import certifi
import ssl
import urllib3
from typing import List, Dict, Tuple, Optional, Union
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pathlib import Path
import subprocess
from urllib.parse import urlparse
from collections import defaultdict

def normalize_url(url: Union[str, List[str]]) -> str:
    """
    Normalize URL to ensure it's a string, not a list.
    
    Args:
        url: URL that might be either a string or a list of strings
        
    Returns:
        str: The normalized URL
    """
    if isinstance(url, list):
        return url[0] if url else ''
    return str(url) if url is not None else ''

class SecureFileDownloadManager:
    def __init__(self, base_path: str = "data/federal/attachments"):
        """
        Initialize the secure file download manager.
        
        Args:
            base_path (str): Base directory for downloaded files
        """
        self.base_path = Path(base_path)
        self.session = self._create_session()
        self.successful_methods = defaultdict(str)  # Track successful methods by domain
        os.makedirs(self.base_path, exist_ok=True)
        self._install_certificates()
        
    def _install_certificates(self):
        """Install certificates on macOS if needed."""
        try:
            if os.path.exists('/Applications/Python 3.10'):
                print("Installing certificates for macOS...")
                cmd = '/Applications/Python 3.10/Install Certificates.command'
                if os.path.exists(cmd):
                    subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"Certificate installation attempt failed: {e}")
            
    def _create_session(self) -> requests.Session:
        """
        Create a session with enhanced SSL handling.
        
        Returns:
            requests.Session: Configured session object
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # Create custom adapter with longer timeouts
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=100,
            pool_maxsize=100
        )
        
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        # Set default verification to use certifi
        session.verify = certifi.where()
        
        return session

    def secure_get(self, url: str, allow_insecure: bool = False) -> Tuple[Optional[requests.Response], str]:
        """
        Make a secure HTTP request with multiple fallback options.
        
        Args:
            url (str): The URL to request
            allow_insecure (bool): Whether to allow insecure connections
            
        Returns:
            Tuple[Optional[requests.Response], str]: The response and the method that succeeded
        """
        domain = urlparse(url).netloc
        errors = []
        
        # Check if we have a successful method for this domain
        if domain in self.successful_methods:
            preferred_method = self.successful_methods[domain]
            if preferred_method == "insecure" and not allow_insecure:
                print(f"Skipping known insecure method for {domain} due to security settings")
            else:
                try:
                    if preferred_method == "certifi":
                        response = self.session.get(url, timeout=30)
                        return response, "certifi"
                    elif preferred_method == "custom_ssl":
                        context = ssl.create_default_context(cafile=certifi.where())
                        response = self.session.get(url, verify=context.get_ca_certs(), timeout=30)
                        return response, "custom_ssl"
                    elif preferred_method == "system":
                        response = self.session.get(url, verify=True, timeout=30)
                        return response, "system"
                    elif preferred_method == "insecure":
                        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                        response = self.session.get(url, verify=False, timeout=30)
                        return response, "insecure"
                except Exception as e:
                    print(f"Preferred method {preferred_method} failed for {domain}: {e}")
        
        # First attempt: Using certifi certificates
        try:
            response = self.session.get(url, timeout=30)
            self.successful_methods[domain] = "certifi"
            return response, "certifi"
        except Exception as e:
            errors.append(f"Default certifi attempt failed: {str(e)}")

        # Second attempt: Using custom SSL context
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            response = self.session.get(url, verify=context.get_ca_certs(), timeout=30)
            self.successful_methods[domain] = "custom_ssl"
            return response, "custom_ssl"
        except Exception as e:
            errors.append(f"Custom SSL context attempt failed: {str(e)}")

        # Third attempt: Using system certificates
        try:
            response = self.session.get(url, verify=True, timeout=30)
            self.successful_methods[domain] = "system"
            return response, "system"
        except Exception as e:
            errors.append(f"System certificates attempt failed: {str(e)}")

        # Final attempt: Insecure connection if allowed
        if allow_insecure:
            try:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                print("WARNING: Making insecure request with SSL verification disabled")
                response = self.session.get(url, verify=False, timeout=30)
                self.successful_methods[domain] = "insecure"
                return response, "insecure"
            except Exception as e:
                errors.append(f"Insecure attempt failed: {str(e)}")

        print(f"All connection attempts failed for URL: {url}")
        for error in errors:
            print(f"  - {error}")
        return None, "failed"

    def download_file(self, file_url: Union[str, List[str]], file_type: str, allow_insecure: bool = False) -> bool:
        """
        Download a single file with enhanced error handling and method tracking.
        
        Args:
            file_url: URL of the file to download
            file_type: Type of file (extension)
            allow_insecure: Whether to allow insecure downloads
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            normalized_url = normalize_url(file_url)
            if not normalized_url:
                print("Invalid URL provided")
                return False
            
            try:
                doc_id = normalized_url.split('/')[-2]
            except IndexError:
                print(f"Could not extract doc_id from URL: {normalized_url}")
                return False
                
            print(f"Downloading file for doc_id: {doc_id}")
            
            # Try multiple times with different SSL configurations
            response = None
            successful_method = None
            
            for attempt in range(3):  # Try 3 times
                response, method = self.secure_get(normalized_url, allow_insecure)
                if response is not None and response.status_code == 200:
                    successful_method = method
                    break
                elif response is not None:
                    print(f"Attempt {attempt + 1} failed with status code: {response.status_code}")
                else:
                    print(f"Attempt {attempt + 1} failed to establish connection")
            
            if response is None:
                print(f"Failed to download {doc_id} after all attempts")
                return False
                
            response.raise_for_status()
            
            file_path = self.base_path / f"{doc_id}.{file_type}"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded {doc_id} using {successful_method} method")
            return True
            
        except Exception as e:
            doc_id = 'unknown'
            try:
                doc_id = normalized_url.split('/')[-2]
            except:
                pass
            print(f"Error downloading {doc_id}: {str(e)}")
            return False

    def process_missing_files(self, missing_df: pd.DataFrame, file_type: str, 
                            allow_insecure: bool = False) -> List[str]:
        """
        Process all missing files of a specific type.
        
        Args:
            missing_df: DataFrame containing missing files
            file_type: Type of files to process
            allow_insecure: Whether to allow insecure downloads
            
        Returns:
            List[str]: List of failed downloads
        """
        missing_files = missing_df[missing_df['fileType'] == file_type]
        file_urls = missing_files['fileUrl'].unique().tolist()
        failed_downloads = []
        
        for file_url in file_urls:
            if not self.download_file(file_url, file_type, allow_insecure):
                failed_downloads.append(normalize_url(file_url))
                
        return failed_downloads

    def analyze_missing_files(self) -> Tuple[Dict, pd.DataFrame]:
        """
        Analyze which files are missing from the downloads.
        
        Returns:
            Tuple[Dict, pd.DataFrame]: Statistics about missing files and the missing files DataFrame
        """
        attachments = get_attachments()
        downloads = get_downloads()
        
        attachments['fileUrl'] = attachments['fileUrl'].apply(normalize_url)
        
        stats = {
            'unique_attachments': attachments['doc_id'].nunique(),
            'unique_downloads': downloads['doc_id'].nunique()
        }
        
        merged = pd.merge(attachments, downloads, on='doc_id', how='left', indicator=True)
        missing = merged[merged['_merge'] == 'left_only'].copy()
        missing['fileUrl'] = missing['fileUrl'].apply(normalize_url)
        
        missing_by_type = missing.groupby('fileType').size()
        stats['missing_by_type'] = missing_by_type.to_dict()
        stats['total_missing'] = missing.shape[0]
        
        return stats, missing

def main():
    """Main function to orchestrate the secure download process."""
    manager = SecureFileDownloadManager()
    
    stats, missing = manager.analyze_missing_files()
    print("\nInitial Analysis:")
    print(f"Unique attachments: {stats['unique_attachments']}")
    print(f"Unique downloads: {stats['unique_downloads']}")
    print(f"Missing files by type: {stats['missing_by_type']}")
    
    file_types = ['htm', 'pdf', 'docx']
    failed_by_type = {}
    
    # Try with both secure and insecure connections immediately
    print("\nAttempting downloads with all available methods...")
    for file_type in file_types:
        print(f"\nProcessing {file_type} files...")
        failed = manager.process_missing_files(missing, file_type, allow_insecure=True)
        failed_by_type[file_type] = failed
        
        stats, missing = manager.analyze_missing_files()
        print(f"Remaining missing files: {stats['total_missing']}")
    
    # Final report
    print("\nDownload Summary:")
    print("\nSuccessful methods by domain:")
    for domain, method in manager.successful_methods.items():
        print(f"  {domain}: {method}")
    
    print("\nFailed downloads by type:")
    for file_type, failed in failed_by_type.items():
        print(f"{file_type}: {len(failed)} failed downloads")
        if failed:
            print("Failed URLs:")
            for url in failed:
                print(f"  {url}")

if __name__ == "__main__":
    main()