import os
import requests
import pandas as pd
import markdown

import sys
# adding to the system path
sys.path.insert(0, '/Users/bluebird/develop/reg_extract/')
from testing.send_folder_to_ai import folder_to_ai

from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    # Supabase credentials
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    print("Supabase client created successfully.")
except Exception as e:
    print(f"Error creating Supabase client: {e}")

# Fetch data from Supabase
response = supabase.table("ea_fdic").select("*").order("issued_date", desc=True).execute()
df = pd.DataFrame(response.data)
print(df.head())

path = '/Users/bluebird/develop/reg_extract/data/enforcement_actions/documents/fdic'
summaries = folder_to_ai(path)

# Join the summaries to the dataframe on file_name
ai_df = pd.DataFrame(summaries)
# Remove .DS_Store file
ai_df = ai_df[ai_df['file_name'] != '.DS_Store']
# Remove .pdf from file_name
ai_df['file_name'] = ai_df['file_name'].str.replace('.pdf', '')

# Export to csv
ai_df.to_csv('data/enforcement_actions/fdic_ai_summaries.csv', index=False)

# Update the Supabase table with the AI summaries
for index, row in ai_df.iterrows():
    try:
        supabase.table("ea_fdic").update({"ai_summary": row['summary']}).match({"file_name": row['file_name']}).execute()
        print(f"Updated AI summary for {row['file_name']}")
    except Exception as e:
        print(f"Error updating AI summary for {row['file_name']}: {e}")

