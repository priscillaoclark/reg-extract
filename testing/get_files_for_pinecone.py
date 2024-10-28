from _03_mongodb import get_documents
import pandas as pd
# Connect to supabase
from supabase import create_client, Client
from dotenv import load_dotenv
import os

def get_files_for_pinecone():
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
    response = supabase.table("federal_documents").select("*").execute().data
    response_2 = supabase.table("federal_documents_attachments").select("*").execute().data

    # Convert the response data to a pandas DataFrame
    df = pd.DataFrame(response)
    df_files = pd.DataFrame(response_2)

    # Join the two DataFrames on the doc_id column
    df_merged = pd.merge(df, df_files, on='doc_id', how='inner')

    # Filter the merged DataFrame for postedDate after 2023
    df_merged_2024 = df_merged[df_merged['postedDate'] >= '2024-01-01']

    # Filter the merged DataFrame for documents with a fileUrl
    df_merged_2024_files = df_merged_2024[df_merged_2024['fileUrl'].notna()]

    # Filter out notices
    df_merged_2024_files = df_merged_2024_files[~df_merged_2024_files['documentType'].str.contains("Notice")]

    # Count the number of documents in the filtered DataFrame
    #print(df_merged_2024_files.shape)
    #print(df_merged_2024_files.head())

    # Add htm files to a new DataFrame
    df_htm = df_merged_2024_files[df_merged_2024_files['format'] == 'htm']
    # Convert the fileUrl to just the filename
    df_htm['fileUrl'] = df_htm['fileUrl'].str.split('/').str[-2] + '.htm'
    # Add pdf files if the doc_id is not in the htm DataFrame
    df_pdf = df_merged_2024_files[~df_merged_2024_files['doc_id'].isin(df_htm['doc_id'])]
    df_pdf['fileUrl'] = df_pdf['fileUrl'].str.split('/').str[-2] + '.pdf'

    # Print the number of htm and pdf files
    #print(df_htm.shape)
    #print(df_pdf.shape)

    # Create a combined list of fileUrls
    fileUrls = df_htm['fileUrl'].tolist() + df_pdf['fileUrl'].tolist()
    #print(len(fileUrls))
    fileUrls = fileUrls[:20]
    print("Number of files:", len(fileUrls))
    
    # Limit to 5 files for testing
    return fileUrls

    #return fileUrls
