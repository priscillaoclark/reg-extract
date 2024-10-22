import os
import requests
import pandas as pd
import markdown

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

# Fetch data from Supabase
response = supabase.table("ea_frb").select("*").order("effective_date", desc=True).execute()
df = pd.DataFrame(response.data)

# Limit rows for testing
df = df.head(10)
#print(df)

# ai_summary = []

# Test update - need to remove RLS for permisison
#supabase.table("ea_frb").update({"ai_summary": ""}).match({"url": "https://www.federalreserve.gov/boarddocs/press/enforcement/2000/200001192/default.htm"}).execute()

# Iterate through the DataFrame and download files
for index, row in df.iterrows():
        try:
            if not row['ai_summary']:
                print(f"Summarizing {row['url']}")
                summary = link_to_ai(row['url'])
                #summary_html = markdown.markdown(summary)
                #ai_summary.append({'link': row['url'], 'summary': summary})
                # Check if the ai_summary in the row is empty
                supabase.table("ea_frb").update({"ai_summary": summary}).match({"url": row['url']}).execute()
            else:
                print(f"AI summary already exists for {row['url']} - skipping.")
        except Exception as e:
            print(f"Error sending {row['url']} to AI: {e}")
    
# Save the AI summaries to a CSV file
#ai_df = pd.DataFrame(ai_summary)
#ai_df.to_csv("/Users/bluebird/develop/reg_extract/data/enforcement_actions/frb_ai_summaries.csv", index=False)

"""
# Update the Supabase table with the AI summaries
for index, row in ai_df.iterrows():
    try:
        supabase.table("ea_frb").update({"ai_summary": row['summary']}).match({"url": row['link']}).execute()
        print(f"Updated AI summary for {row['link']}")
    except Exception as e:
        print(f"Error updating AI summary for {row['link']}: {e}")
"""

