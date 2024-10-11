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
  
def get_documents():  
    client = connect_to_mongodb()

    reg_data = client["reg_data"]
    federal_documents = reg_data["federal_documents"]

    """
    search_id = 'FHFA-2024-0022-0001'
    # Find one document by ID
    response = federal_documents.find_one({"data.id": search_id})
    print(type(response))
    print(response.get('data').get('attributes').get('title'))
    """

    documents = []

    # Find all documents with a postedDate of 2024-10-01
    # response_2 = federal_documents.find({'data.attributes.postedDate': {'$gte':"2024-10-01",'$lt':"2024-10-02"}})
    response = federal_documents.find()
    #print(response)

    for doc in response:

        document = {
            "doc_id": doc.get('data').get('id'),
            "title": doc.get('data').get('attributes').get('title'),
            "agencyId": doc.get('data').get('attributes').get('agencyId'),
            "documentType": doc.get('data').get('attributes').get('documentType'),
            "postedDate": doc.get('data').get('attributes').get('postedDate'),
            "modifyDate": doc.get('data').get('attributes').get('modifyDate'),
            "receiveDate": doc.get('data').get('attributes').get('receiveDate'),
            "withdrawn": doc.get('data').get('attributes').get('withdrawn'),
            "docketId": doc.get('data').get('attributes').get('docketId'),
            "openForComment": doc.get('data').get('attributes').get('openForComment'),
            "commentStartDate": doc.get('data').get('attributes').get('commentStartDate'),
            "commentEndDate": doc.get('data').get('attributes').get('commentEndDate'),
            "frDocNum": doc.get('data').get('attributes').get('frDocNum'),
            "objectId": doc.get('data').get('attributes').get('objectId'),
        }
        
        # Check if the document already exists in the list
        if document not in documents:
            documents.append(document)

    df = pd.DataFrame(documents)

    return df

"""
df = get_documents()
print(df.head())
print(df.shape)
"""