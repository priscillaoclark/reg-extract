from pinecone import Pinecone, ServerlessSpec
import os

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

delete_all_vectors()