import os
import json
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from PyPDF2 import PdfReader
from get_files_for_pinecone import get_files_for_pinecone
from bs4 import BeautifulSoup
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd

def get_embeddings(text):
    # Initialize OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding

def chunk_text(text, chunk_size=3000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
    
def upload_file_and_get_embeddings(file_path):
    # Determine file extension and read content accordingly
    file_name = os.path.basename(file_path).split('/')[-1].split('.')[0]
    extension = os.path.basename(file_path).split('.')[-1]

    if extension == "pdf":
        # Read PDF content
        content = ""
        try:
            with open(file_path, "rb") as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    content += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading PDF file '{file_name}': {e}")
            return []
    else:
        # Read text file content
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                # Remove html tags and special characters
                # Remove HTML tags
                soup = BeautifulSoup(content, "html.parser")
                content = soup.get_text()

                # Remove special characters and extra whitespace
                content = content.replace("\n", " ").replace("\r", " ").replace("\t", " ")
                content = " ".join(content.split())
                
        except Exception as e:
            print(f"Error reading text file '{file_name}': {e}")
            return []

    # Chunk the content and generate embeddings
    chunks = chunk_text(content)
    vectors = []

    for i, chunk in enumerate(chunks):
        try:
            print(f"Generating embeddings for chunk {i+1} of '{file_name}'...")
            embeddings = get_embeddings(chunk)
            vectors.append({
                "id": f"{file_name}_vec{i+1}",
                "values": embeddings,
                "metadata": {"filename": file_name, "extension": extension}
            })
        except Exception as e:
            print(f"Error generating embeddings for chunk {i+1} of '{file_name}': {e}")
            continue  # Skip this chunk if there's an error
    return vectors

def upsert_pinecone(file_path):
    # Initialize Pinecone
    try:
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Create or connect to an index
        index_name = "test-index"
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name, 
                dimension=1536,  # Ensure this matches the embedding dimension from OpenAI
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-west-2'
                )
            )
        index = pc.Index(index_name)
    except Exception as e:
        print(f"Error connecting to Pinecone: {e}")
        return

    # Extract file information and create a unique ID prefix based on filename
    file_name = os.path.basename(file_path).split('.')[0]
    unique_id_prefix = f"{file_name}_vec"

    # Check if vectors with this filename prefix already exist in Pinecone
    try:
        existing_vector = index.fetch(ids=[unique_id_prefix + "1"], namespace="major-regs")
        if existing_vector.vectors:
            print(f"File '{file_name}' already exists in the Pinecone index. Skipping.")
            return
    except Exception as e:
        print(f"Error fetching vector by ID for '{file_name}': {e}")
        return

    # Get embeddings and prepare data for upsert
    try:
        vectors = upload_file_and_get_embeddings(file_path)
        if not vectors:
            print(f"Error: No content extracted or processed for file '{file_name}'. Skipping.")
            return
    except Exception as e:
        print(f"Error uploading file and getting embeddings for '{file_name}': {e}")
        return
    # If there are more than 150 vectors, split into batches of 200
    if len(vectors) > 150:
        for i in range(0, len(vectors), 150):
            try:
                index.upsert(vectors=vectors[i:i+150], namespace="major-regs")
                print(f"Batch {i//150 + 1} of vectors for '{file_name}' successfully upserted into Pinecone.")
            except Exception as e:
                print(f"Error upserting data for '{file_name}': {e}")
    else:
        # Upsert data into Pinecone
        try:
            index.upsert(vectors=vectors, namespace="major-regs")
            print(f"File '{file_name}' successfully upserted into Pinecone.")
        except Exception as e:
            print(f"Error upserting data for '{file_name}': {e}")

# Process all files in a directory
#directory = "/Users/bluebird/develop/reg_extract/data/federal/attachments/testing"
directory = "/Users/bluebird/develop/reg_extract/data/regs"

# Get all files in the directory
files = os.listdir(directory)

for filename in files:
    file_path = os.path.join(directory, filename)
    try:
        if filename.endswith((".htm", ".pdf")):
            upsert_pinecone(file_path)
        else:
            print(f"Skipping unsupported file type for '{filename}'")
            continue
    except Exception as e:
        print(f"Error processing file '{filename}': {e}")
        continue
