import os
import requests
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from _03_mongodb import get_documents
# https://sysadmins.co.za/mongodb-cheatsheet-with-pymongo/

# Get the API key from the .env file
from dotenv import load_dotenv

def connect_to_mongodb():
    load_dotenv()

    # MongoDB connection string
    MONGO_URI = os.getenv("ATLAS_URI")
    try:
        # Create a new client and connect to the server
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def get_mongodb_attachments():
    client = connect_to_mongodb()

    reg_data = client["reg_data"]
    federal_documents_attachments = reg_data["federal_documents_attachments"]

    documents = []

    response = federal_documents_attachments.find()
    #print(response)

    for doc in response:
        #print(doc)
        document = {
            "filename": doc.get('filename'),
            "doc_id": doc.get('doc_id'),
            "doc_size": doc.get('doc_size'),
            "extension": doc.get('extension'),
            "num_words": doc.get('num_words'),
            "num_unique_words": doc.get('num_unique_words'),
            "title": doc.get('title'),
            "num_links": doc.get('num_links'),
            "links": doc.get('links'),
            "agency": doc.get('agency'),
            "action": doc.get('action'),
            "doc_summary": doc.get('doc_summary'),
            "ai_summary_short": doc.get('ai_summary_short'),
            "ai_summary_long": doc.get('ai_summary_long')
    }
               
        documents.append(document)

    df = pd.DataFrame(documents)

    return df

# Example usage
df = get_mongodb_attachments()
# Count the number of documents
#print(df.shape[0])
# Clean up doc ID column - pull the ID from the URL
df['doc_id'] = df['doc_id'].str.split('/').str[-1]
#print(df.head())

# Bring in document metadata
metadata = get_documents()
metadata_df = pd.DataFrame(metadata)

# Merge the two dataframes on the doc_id column
df_combined = pd.merge(df, metadata_df, on='doc_id', how='inner')
#print(df_combined.head())
#print(df_combined.columns)

# Print the doc_id and ai_summary_short for each document
for index, row in df_combined.iterrows():
    print(f"""Doc ID: {row['doc_id']}\n
          Date Posted: {row['postedDate']}\n
          Title: {row['title_y']}\n
          Agency: {row['agency']}\n
          Document Type: {row['documentType']}\n
          AI Summary: {row['ai_summary_short']}\n
          Document Summary: {row['doc_summary']}\n
          --------------------------------------------------\n
          """)