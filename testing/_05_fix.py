import os
import requests
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Get the API key from the .env file
from dotenv import load_dotenv
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("ATLAS_URI")

# Get API key from environment variable
API_KEY = os.getenv("REGULATIONS_GOV_API_KEY")
BASE_URL = "https://api.regulations.gov/v4"

def connect_to_mongodb():
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

def get_document_details(document_id):
    endpoint = f"{BASE_URL}/documents/{document_id}"
    params = {
        "api_key": API_KEY,
        "include": "attachments"
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def load_json_to_mongodb(json_data, collection):
    try:
        collection.insert_one(json_data)
    except Exception as e:
        print(f"Error inserting document: {e}")

def upload_single_document(doc_id, collection):
    # Connect to MongoDB
    client = connect_to_mongodb()
    if not client:
        print("Failed to connect to MongoDB. Exiting.")
        exit(1)

    DB_NAME = "reg_data"
    COLLECTION_NAME = collection

    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    details = get_document_details(doc_id)
    if details:
        # save_json(details, f"data/federal/document_details/{startDate}_{doc_id}.json")
        load_json_to_mongodb(details, collection)