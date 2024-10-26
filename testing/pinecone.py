import os
from openai import OpenAI
import json
from pinecone.grpc import PineconeGRPC as Pinecone

try:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("test-index")
except Exception as e:
    print(f"Error connecting to Pinecone: {e}")

# Load your OpenAI API key from an environment variable or secret management service
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def get_embeddings(text):
    response = client.embeddings.create(input=text,
    model="text-embedding-3-small")
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
    with open(file_path, 'r') as file:
        content = file.read()
    chunks = chunk_text(content)
    vectors = []
    # Get file name without the extension
    file_name = os.path.basename(file_path).split('.')[0]
    extension = os.path.basename(file_path).split('.')[1]
    # Get first 4 characters of the file name
    agency = file_name[:4]
    # Replace underscores with spaces
    agency = agency.replace("_", "")
    #Replace dashes with spaces
    agency = agency.replace("-", "")
    
    for i, chunk in enumerate(chunks):
        embeddings = get_embeddings(chunk)
        vectors.append({
            "id": f"vec{i+1}",
            "values": embeddings,
            "metadata": {"filename": os.path.basename(file_name), "extension": extension, "agency": agency}
        })
    return {
        "vectors": vectors,
        "namespace": "federal-documents"
    }

# Example usage
file_path = "/Users/bluebird/develop/reg_extract/data/federal/attachments/CCC_FRDOC_0001-0409.htm"
try:
    result = upload_file_and_get_embeddings(file_path)
    upsert_data = json.dumps(result, indent=2)
except Exception as e:
    print(f"Error uploading file and getting embeddings: {e}")
#print(json.dumps(result, indent=2))

# Upsert data into a specific namespace
try:
    index.upsert([
        upsert_data
    ])
except Exception as e:
    print(f"Error upserting data: {e}")
    
# Query data from the specific namespace
#results = index.query(queries=[[0.1, 0.2, 0.3]], namespace="ns1")
#print(results)
