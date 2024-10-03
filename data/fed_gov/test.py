import os
# Get API key from environment variable
API_KEY = os.getenv("REGULATIONS_GOV_API_KEY")
print(API_KEY)
MONGO_URI = os.getenv("ATLAS_URI")
print(MONGO_URI)

from pymongo import MongoClient
from pymongo.server_api import ServerApi
import ssl
import certifi

# MongoDB connection string
MONGO_URI = os.getenv("ATLAS_URI")

def connect_to_mongodb():
    try:
        # Attempt 1: Default connection
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(f"Default connection failed: {e}")
        try:
            # Attempt 2: Use certifi's SSL certificate
            client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tls=True, tlsCAFile=certifi.where())
            client.admin.command('ping')
            print("Successfully connected to MongoDB using certifi!")
            return client
        except Exception as e:
            print(f"Certifi connection failed: {e}")
            try:
                # Attempt 3: Disable SSL certificate verification (not recommended for production)
                client = MongoClient(MONGO_URI, server_api=ServerApi('1'), ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
                client.admin.command('ping')
                print("Successfully connected to MongoDB with SSL verification disabled!")
                return client
            except Exception as e:
                print(f"All connection attempts failed. Final error: {e}")
                return None

connect_to_mongodb()