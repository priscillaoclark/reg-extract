import os
import requests
import pandas as pd

# https://www.federalreserve.gov/supervisionreg/enforcementactions.htm

# Define the base URL
base_url = "https://www.federalreserve.gov"

# Load the CSV file
csv_path = "/Users/bluebird/develop/reg_extract/data/enforcement_actions/frb_enforcementactions.csv"
df = pd.read_csv(csv_path)

# Function to download file
def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    filename = os.path.join(dest_folder, url.split("/")[-1])
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Iterate through the DataFrame and download files
for index, row in df.iterrows():
    link = row['URL']
    if link != 'DNE':
        try:
            if link.startswith("/"):
                link = base_url + link
                # Check to see if file has already been downloaded
                filename = link.split("/")[-1]
                if not os.path.exists(f"/Users/bluebird/develop/reg_extract/data/enforcement_actions/documents/frb/{filename}"):
                    print(f"Downloading {link}")
                    download_file(link, "/Users/bluebird/develop/reg_extract/data/enforcement_actions/documents/frb")
                else:
                    print(f"File {filename} already exists - skipping download.")
        except Exception as e:
            print(f"Error downloading {link}: {e}")

