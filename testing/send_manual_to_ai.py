import sys
sys.path.insert(0, '/Users/bluebird/develop/reg_extract/')
from testing.llm_summary import get_ai_summaries
import os
from PyPDF2 import PdfReader
import pandas as pd

def send_manual_to_ai(folder, assistant_id, field):
    #print(folder)
        
    for filename in os.listdir(folder):
        if filename != '.DS_Store':
            file = str(filename).split('/')[-1]
            file = file.split('.')[0]
            file = file[2:]
            #print(file)
            #print(filename)
            full_path = os.path.join(folder, filename)
            print("Processing: ", full_path)

            reader = PdfReader(full_path)
            count = len(reader.pages)

            output = []
            for i in range(count):
                page = reader.pages[i]
                output.append(page.extract_text())

            combined = ','.join(output)
            ai_summary = get_ai_summaries(combined, assistant_id)
            ai_summary_short, ai_summary_long = ai_summary
            #ai_summary_short = 'test'

            data = {'file_name': file, 'summary': ai_summary_short}
            # Convert dictionary to dataframe
            df = pd.DataFrame(data, index=[0])
            #print(df.head())

            # Save to CSV
            #df.to_csv(f'/Users/bluebird/develop/reg_extract/data/enforcement_actions/occ_{file}.csv', mode='a', header=False, index=False)

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
                if field == 'summary':
                    supabase.table("ea_occ").update({"ai_summary": row['summary']}).match({"start_documents": row['file_name']}).execute()
                if field == 'keyword':
                    supabase.table("ea_occ").update({"keywords": row['summary']}).match({"start_documents": row['file_name']}).execute()

# USE FUNCTION

# PICK ASSISTANT
#assistant_id = "asst_NbCGwXBaXWbRQr683B9fT0H3" # Proposed rules
#assistant_id = "asst_LI1IMVCPdu6g0P4Io3s5gr1H" # EA
assistant_id = "asst_xyi5cX9PnYyJ0IwxpBfXDc1z" # Keywords

field = 'keyword'
folder = '/Users/bluebird/develop/reg_extract/data/enforcement_actions/documents/occ/'
send_manual_to_ai(folder, assistant_id, field)

