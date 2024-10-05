import os
import requests
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from parse_doc import summarize_attachments

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

def search_documents(startDate, endDate, document_type=None, docket_id=None, search_term=None, agency_id=None):
    endpoint = f"{BASE_URL}/documents"
    params = {
        "api_key": API_KEY,
        "filter[postedDate][ge]": startDate,
        "filter[postedDate][le]": endDate,
        "sort": "-postedDate",
        "page[size]": 250  # Max results for API
    }
    if document_type:
        params["filter[documentType]"] = document_type
    if docket_id:
        params["filter[docketId]"] = docket_id
    if search_term:
        params["filter[searchTerm]"] = search_term
    if agency_id:
        params["filter[agencyId]"] = agency_id
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def save_json(response, filename):
    with open(filename, 'w') as f:
        json.dump(response, f, indent=4)

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

def extract_federal():
    # Get yesterday's date
    startDate = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    #startDate = '2024-10-01'
    endDate = startDate
    search_term = None
    document_id = None
    docket_id = None

    # Connect to MongoDB
    client = connect_to_mongodb()
    if not client:
        print("Failed to connect to MongoDB. Exiting.")
        exit(1)
    
    DB_NAME = "reg_data"
    COLLECTION_NAME = "federal_documents"
    
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Import agency IDs from agencies.json
    try:
        with open("data/federal/agencies.json") as f:
            agencies = json.load(f)
    except FileNotFoundError:
        print("agencies.json file not found. Please ensure it exists in the data/ directory.")
        exit(1)

    # Convert the list of agencies to a list of agency IDs
    agency_ids = [agency['agency_id'] for agency in agencies]

    for agency_id in agency_ids:
        response = search_documents(startDate=startDate, endDate=endDate, document_type=document_id, docket_id=docket_id, search_term=search_term, agency_id=agency_id)
        if response:
            document_ids = [doc['id'] for doc in response['data']]
            # Check to see if documents were returned
            if len(document_ids) == 0:
                print(f"No documents found for {agency_id}")
            else:
                print(f"{len(document_ids)} documents found for {agency_id}")
                save_json(response, f"data/federal/documents/{startDate}_{agency_id}.json")
                #load_json_to_mongodb(response, collection_1)

                # Save the details for each document to a separate JSON file and load into MongoDB
                for doc_id in document_ids:
                    details = get_document_details(doc_id)
                    if details:
                        # save_json(details, f"data/federal/document_details/{startDate}_{doc_id}.json")
                        load_json_to_mongodb(details, collection)
                       
                # Download the htm file listed in the link in fileFormats
                try:
                    for doc_id in document_ids:
                        details = get_document_details(doc_id)
                        if details:
                            if details['data']['attributes'] and 'fileFormats' in details['data']['attributes']:
                                for attachment in details['data']['attributes']['fileFormats']:
                                    if attachment['fileUrl'].endswith('.htm'):
                                        response = requests.get(attachment['fileUrl'])
                                        output_file_html = f"data/federal/attachments/{doc_id}.htm"
                                        with open(output_file_html, 'wb') as f:
                                            f.write(response.content)
                                        try:
                                            summarize_attachments(output_file_html)
                                        except Exception as e:
                                            print(f"Error summarizing attachments for {doc_id}: {e}")
                                            continue
                                    """if attachment['fileUrl'].endswith('.pdf'):
                                        response = requests.get(attachment['fileUrl'])
                                        output_file_pdf = f"data/federal/attachments/{doc_id}.pdf"
                                        with open(output_file_pdf, 'wb') as f:
                                            f.write(response.content)
                                        try:
                                            summarize_attachments(output_file_pdf)
                                        except Exception as e:
                                            print(f"Error summarizing attachments for {doc_id}: {e}")
                                            continue"""
                except Exception as e:
                    print(f"Error downloading attachments for {agency_id}: {e}")
                
            # List the number of documents returned for each agency to a log file
            with open(f"data/federal/logs/{startDate}_log.txt", "a") as f:
                f.write(f"{agency_id}: {len(document_ids)}\n")
                f.write("---\n")

    # Close the MongoDB connection
    client.close()