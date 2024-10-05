import os
import requests
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
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

def get_attachments():
    client = connect_to_mongodb()

    reg_data = client["reg_data"]
    federal_documents = reg_data["federal_documents"]
    federal_documents_history = reg_data["federal_documents_history"]

    """
    search_id = 'FHFA-2024-0022-0001'
    # Find one document by ID
    response = federal_documents.find_one({"data.id": search_id})
    print(type(response))
    print(response.get('data').get('attributes').get('title'))
    """

    documents = []

    response = federal_documents.find()
    #print(response)

    for doc in response:
        doc_id = doc.get('data').get('id')
        postedDate = doc.get('data').get('attributes').get('postedDate')
        try:  
            fileTypes = doc.get('data').get('attributes').get('fileFormats')
            #print(fileTypes)
            for doc in fileTypes:
                #print(doc.get('fileUrl'))
                document = {
                "doc_id": doc_id,
                "fileUrl": doc.get('fileUrl'),
                "fileType": doc.get('format'),
                "postedDate": postedDate
                }
            
                # Check if the document already exists in the list
                if document not in documents:
                    documents.append(document)
        except Exception as e:
            print(f"Error downloading attachments for {doc_id}: {e}")
            continue

    response_history = federal_documents_history.find()
    #print(response)

    for doc in response_history:
        doc_id = doc.get('data').get('id')
        postedDate = doc.get('data').get('attributes').get('postedDate')
        try:  
            fileTypes = doc.get('data').get('attributes').get('fileFormats')
            #print(fileTypes)
            for doc in fileTypes:
                #print(doc.get('fileUrl'))
                document = {
                "doc_id": doc_id,
                "fileUrl": doc.get('fileUrl'),
                "fileType": doc.get('format'),
                "postedDate": postedDate
                }
            
                # Check if the document already exists in the list
                if document not in documents:
                    documents.append(document)
        except Exception as e:
            print(f"Error downloading attachments for {doc_id}: {e}")
            continue

    df = pd.DataFrame(documents)

    return df

"""
df = get_attachments()
# Count the number of documents
print(df.shape[0])

# Sort the documents by postedDate
df = df.sort_values(by='postedDate')
print(df.head())
"""