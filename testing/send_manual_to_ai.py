import sys
sys.path.insert(0, '/Users/bluebird/develop/reg_extract/')
from testing.llm_summary import get_ai_summaries
import os
from PyPDF2 import PdfReader
import pandas as pd

filename = '/Users/bluebird/develop/reg_extract/data/enforcement_actions/documents/fdic/24-0051k.pdf'
reader = PdfReader(filename)
count = len(reader.pages)

output = []
for i in range(count):
    page = reader.pages[i]
    output.append(page.extract_text())

combined = ','.join(output)
print(combined)
ai_summary = get_ai_summaries(combined)
ai_summary_short, ai_summary_long = ai_summary
#ai_summary_short = 'test'

file = str(filename).split('/')[-1]
file = file.split('.')[0]
data = {'file_name': file, 'summary': ai_summary_short}
# Convert dictionary to dataframe
df = pd.DataFrame(data, index=[0])
print(df.head())

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

# Loop through the dataframe and update the Supabase table
for index, row in df.iterrows():
    supabase.table("ea_fdic").update({"ai_summary": row['summary']}).match({"file_name": row['file_name']}).execute()