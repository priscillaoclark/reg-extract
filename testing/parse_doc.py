import os
import pandas as pd
from bs4 import BeautifulSoup
from openai import OpenAI
import re
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import PyPDF2
from llm_summary import get_ai_summaries

def extract_fields(text):
    fields = {
        'AGENCY': r'AGENCY:\s*(.*?)(?=ACTION:)',
        'ACTION': r'ACTION:\s*(.*?)(?=SUMMARY:)',
        'SUMMARY': r'SUMMARY:\s*(.*?)(?=DATES:)'
    }

    results = {}
    for field, pattern in fields.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            results[field] = match.group(1).strip()
        else:
            results[field] = "Not found"

    return results

def summarize_attachments(filename):
    # Connect to MongoDB
    # MongoDB connection string
    MONGO_URI = os.getenv("ATLAS_URI")

    try:
        # Create a new client and connect to the server
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        
    DB_NAME = "reg_data"
    COLLECTION_NAME = "federal_documents_attachments"

    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
        
    # Message console describing which file is being processed
    print(f"Processing file: {filename}")
    
    # Handle HTML files
    if filename.endswith(".htm"):
        with open(filename, 'r') as file:
            contents = file.read()
        
        # Parse the HTML content
        soup = BeautifulSoup(contents, 'html.parser')
        # Find the title of the document
        if soup.find('title'):
            title = soup.find('title').text
        else:
            title = "Not found"
            
        # Find the body of the document
        if soup.find('body'):
            body = soup.find('body').text
            
            # Extract the fields from the document
            fields = extract_fields(body)
            agency = fields['AGENCY']
            action = fields['ACTION']
            summary = fields['SUMMARY']

        else:
            body = "Not found"
            agency = "Not found"
            action = "Not found"
            summary = "Not found"

        # Create a container to store the links
        links = []
        # Loop through each link
        for link in soup.find_all('a'):
            # Get the URL
            url = link.get('href')
            # Append the URL to the list
            links.append(url)
            
    # Handle PDF files  
    if filename.endswith(".pdf"):
        with open(filename, 'rb') as file:
            pdf_contents = PyPDF2.PdfReader(file)
            # Convert the PDF to text
            contents = ""
            for page in pdf_contents.pages:
                contents += page.extract_text()
        
        body = "Not found"
        agency = "Not found"
        action = "Not found"
        summary = "Not found"
        links = []
        title = "Not found"
    
    # Strip the doc ID from the filename
    doc_id = filename.split('.')[0]
    doc_id = doc_id.split('/')[-1]
    
    # Get the total number of words in the document
    num_words = len(contents.split())
    # Get the total number of unique words in the document
    num_unique_words = len(set(contents.split()))
    # Get the file extension
    extension = os.path.splitext(filename)[1]
    
    # Send the file to OpenAI for analysis
    ai_summary = get_ai_summaries(contents)
    if ai_summary:
        ai_summary_short, ai_summary_long = ai_summary
    else:
        # Print error message and exit
        print("Error generating AI summaries. Exiting program.")
        exit(1)
    
    # Add all fields to dictionary
    output = {
        "filename": filename,
        "doc_id": doc_id,
        "doc_size": os.path.getsize(filename),
        "extension": extension,
        "num_words": num_words,
        "num_unique_words": num_unique_words,
        "title": title,
        "num_links": len(links),
        "links": links,
        #"body": body,
        "agency": agency,
        "action": action,
        "doc_summary": summary,
        "ai_summary_short": ai_summary_short,
        "ai_summary_long": ai_summary_long

    }
    
    # Insert the document into the MongoDB collection
    try:
        collection.insert_one(output)
        print("Document inserted successfully!")
    except Exception as e:
        print(f"Error inserting document: {e}")

    # Close the MongoDB connection
    client.close()
