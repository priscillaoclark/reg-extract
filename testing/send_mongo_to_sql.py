from _03_mongodb import get_documents
import pandas as pd
# Connect to supabase
from supabase import create_client, Client
from dotenv import load_dotenv
import os


def send_mongo_to_sql(data):
    df = data
    # print(df.head())
    # print(df.shape)
    # print(df.columns)

    # Parse the file formats to multiple columns
    df_files = df.explode('files')
    df_files = df_files[df_files['files'].notna()]
    df_files = pd.DataFrame(df_files['files'].tolist(), index=df_files.doc_id)
    # print(df_files.head())
    # print(df_files.shape)
    # print(df_files.columns)

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

    # Check for existing documents in the federal_documents_attachments table
    response_2 = supabase.table("federal_documents_attachments").select("fileUrl").execute().data
    # Count rows in the federal_documents table
    print(len(response_2))
    existing_attachments_2 = [item['fileUrl'] for item in response_2]
    # Convert the fileUrl column to a list
    loaded_attachments = df_files['fileUrl'].tolist()
    # Count loaded attachments
    print(len(set(loaded_attachments)))
    # See which fileUrls are not in the existing_attachments list
    new_attachments = [item for item in loaded_attachments if item not in existing_attachments_2]
    # Filter the df_files dataframe to only include the new attachments
    df_files_new = df_files[df_files['fileUrl'].isin(new_attachments)]
    print(df_files_new.shape)

    # Loop through df_files and insert into the federal_documents_attachments table
    for index, row in df_files_new.iterrows():
        data = {
            "doc_id": index,
            "fileUrl": row['fileUrl'],
            "format": row['format'],
            "size": row['size'],
            "ai_summary_short": "TBD",
            "ai_summary_long": "TBD",
            "keywords": "TBD",
        }
        
        try:
            response = supabase.table("federal_documents_attachments").insert(data).execute()
            print(f"Inserted document {index} successfully.")
        except Exception as e:
            print(f"Error inserting document {index}: {e}")

    # Check for existing documents in the federal_documents table
    response = supabase.table("federal_documents").select("doc_id").execute().data
    print(len(response))
    existing_documents = [item['doc_id'] for item in response]
    loaded_documents = df['doc_id'].tolist()
    print(len(set(loaded_documents)))
    new_documents = [item for item in loaded_documents if item not in existing_documents]
    df_documents_new = df[df['doc_id'].isin(new_documents)]
    print(df_documents_new.shape)

    # Loop through df_files and insert into the federal_documents table
    for index, row in df_documents_new.iterrows():
        data = {
            "doc_id": row['doc_id'],
            "title": row['title'],
            "agencyId": row['agencyId'],
            "documentType": row['documentType'],
            "postedDate": row['postedDate'],
            "modifyDate": row['modifyDate'],
            "receiveDate": row['receiveDate'],
            "withdrawn": row['withdrawn'],
            "docketId": row['docketId'],
            "openForComment": row['openForComment'],
            "commentStartDate": row['commentStartDate'],
            "commentEndDate": row['commentEndDate'],
            "frDocNum": row['frDocNum'],
            "objectId": row['objectId'],
            "topics": row['topics'],
            "files": row['files'],
            "relevant": None,
        }
        
        try:
            response = supabase.table("federal_documents").insert(data).execute()
            print(f"Inserted document {row['doc_id']} successfully.")
        except Exception as e:
            print(f"Error inserting document {row['doc_id']}: {e}")

df = get_documents()
send_mongo_to_sql(df)