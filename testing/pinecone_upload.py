import os
import json
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from PyPDF2 import PdfReader

def get_embeddings(text):
    # Initialize OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
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
    agency = file_name[:4].replace("_", "").replace("-", "")

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
        except Exception as e:
            print(f"Error reading text file '{file_name}': {e}")
            return []

    # Chunk the content and generate embeddings
    chunks = chunk_text(content)
    vectors = []

    for i, chunk in enumerate(chunks):
        try:
            embeddings = get_embeddings(chunk)
            vectors.append({
                "id": f"{file_name}_vec{i+1}",
                "values": embeddings,
                "metadata": {"filename": file_name, "extension": extension, "agency": agency}
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
        existing_vector = index.fetch(ids=[unique_id_prefix + "1"], namespace="federal-documents")
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

    # Upsert data into Pinecone
    try:
        index.upsert(vectors=vectors, namespace="federal-documents")
        print(f"File '{file_name}' successfully upserted into Pinecone.")
    except Exception as e:
        print(f"Error upserting data for '{file_name}': {e}")

# Process all files in a directory
directory = "/Users/bluebird/develop/reg_extract/data/federal/attachments/testing"

for filename in os.listdir(directory):
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

"""
def delete_all_vectors():
    # Initialize Pinecone
    try:
        PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Connect to the index
        index_name = "test-index"
        index = pc.Index(index_name)
        
        # Delete all vectors in the specified namespace
        namespace = "federal-documents"
        index.delete(namespace=namespace, delete_all=True)
        print(f"All vectors in namespace '{namespace}' have been deleted from the '{index_name}' index.")
    except Exception as e:
        print(f"Error deleting vectors: {e}")

delete_all_vectors()"""