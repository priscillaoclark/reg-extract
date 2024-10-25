# https://apps.occ.gov/EASearch
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
# adding to the system path
sys.path.insert(0, '/Users/bluebird/develop/reg_extract/')
from testing.send_link_to_ai import link_to_ai

from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    # Supabase credentials
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(url, key)
    print("Supabase client created successfully.")
except Exception as e:
    print(f"Error creating Supabase client: {e}")
    
# Get documents from supabase
response = supabase.table('ea_occ').select("url").order("start_date", desc=True).limit(10).execute()
data_list = response.data
urls = [data['url'] for data in data_list]
print(urls)

folder = "/Users/bluebird/develop/reg_extract/data/enforcement_actions/documents/occ/"

# Download PDFs from urls into the folder
for url in urls:
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    filename = url.split('/')[-1]
    try:
        with open(os.path.join(folder, filename), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")


