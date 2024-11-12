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
    #print(df_files.columns)

    # Join the two DataFrames on the doc_id column
    df_merged = pd.merge(df, df_files, on='doc_id', how='inner')

    # Filter the merged DataFrame for postedDate after 2023
    df_merged_2024 = df_merged[df_merged['postedDate'] >= '2024-01-01']

    # Filter the merged DataFrame for documents with a fileUrl
    df_merged_2024_files = df_merged_2024[df_merged_2024['fileUrl'].notna()]

    # Filter out notices
    #df_merged_2024_files = df_merged_2024_files[~df_merged_2024_files['documentType'].str.contains("Notice")]

    # Add htm files to a new DataFrame
    df_htm = df_merged_2024_files[df_merged_2024_files['format'] == 'htm']
    # Convert size to int
    df_htm.loc[:, 'size'] = df_htm['size'].astype(int)
    # Sort by size
    df_htm = df_htm.sort_values('size', ascending=True)
    # Convert the fileUrl to just the filename
    df_htm.loc[:, 'fileUrl'] = df_htm['fileUrl'].str.split('/').str[-2] + '.htm'
    # See size of htm files
    #print(df_htm['size'].head())
    
    # Add pdf files if the doc_id is not in the htm DataFrame
    df_pdf = df_merged_2024_files[~df_merged_2024_files['doc_id'].isin(df_htm['doc_id'])]
    # Convert size to int
    df_pdf.loc[:, 'size'] = df_pdf['size'].astype(int)
    # Sort by size
    df_pdf = df_pdf.sort_values('size', ascending=True)
    df_pdf.loc[:, 'fileUrl'] = df_pdf['fileUrl'].str.split('/').str[-2] + '.pdf'
    #print(df_pdf['size'].head())

    # Create a combined list of fileUrls
    fileUrls = df_htm['fileUrl'].tolist() + df_pdf['fileUrl'].tolist()
    #fileUrls = fileUrls[:350]
    print("Number of files:", len(fileUrls))
    
    # Limit to 5 files for testing
    return fileUrls

# Call the function to get the list of fileUrls
#fileUrls = get_files_for_pinecone()
