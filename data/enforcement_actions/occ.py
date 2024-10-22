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

base_url = "https://apps.occ.gov/EASearch/?Search=&Category=&ItemsPerPage=10&Sort=StartDateDescending"
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find(class_='table stacked-table table-striped')
rows = table.find_all('tr')
all_content = []

for row in rows[1:]:
    cols = row.find_all('td')
    if len(cols) > 0:
        bank_name = cols[0].text.strip()
        charter_number = cols[1].text.strip()
        company = cols[2].text.strip()
        individual = cols[3].text.strip()
        location = cols[4].text.strip()
        type_code = cols[5].text.strip()
        amount = cols[6].text.strip()
        start_date = cols[7].text.strip()
        start_doc = cols[8].find('a')['href'] if cols[8].find('a') else ''
        termination_date = cols[9].text.strip()
        termination_doc = cols[10].find('a')['href'] if cols[10].find('a') else ''
        docket_number = cols[11].text.strip()
        
        all_content.append({
            'bank_name': bank_name,
            'charter_number': charter_number,
            'company': company,
            'individual': individual,
            'location': location,
            'type_code': type_code,
            'amount': amount,
            'start_date': start_date,
            'start_doc': start_doc,
            'termination_date': termination_date,
            'termination_doc': termination_doc,
            'docket_number': docket_number
        })

df = pd.DataFrame(all_content)

# upload to Supabase
response = supabase.table("ea_occ").upsert(all_content, returning="minimal").execute()


"""
# Download all the documents from start_doc links
for i, row in df.iterrows():
    doc_id = row['start_doc'].split('/')[-1].replace('.pdf', '')
    if row['start_doc'].endswith('.pdf'):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(row['start_doc'], headers=headers)
            file = open(f"data/enforcement_actions/documents/occ/{doc_id}.pdf", "wb")
            file.write(response.content)
            file.close()
        except requests.RequestException as e:
            print(f"Error downloading {doc_id}.pdf: {e}")
            continue  # Move to the next row if there's an issue with this link
        
        if response.status_code == 200:
            # Ensure the directory exists
            os.makedirs("data/enforcement_actions/documents/occ", exist_ok=True)
            # Check if the file already exists
            if not os.path.exists(f"data/enforcement_actions/documents/occ/{doc_id}.pdf"):
                with open(f"data/enforcement_actions/documents/occ/{doc_id}.pdf", 'wb') as f:
                    f.write(response.content)
        else:
            print(f"Error downloading {doc_id}.pdf: status code {response.status_code}")
"""