import pandas as pd
import os
import json

def get_summaries():
    documents = []

    """
    filename = "/Users/bluebird/develop/reg_extract/data/federal/documents/2024-01-01_CFPB.json"
    # Open and read the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)

    for doc in data['data']:
        print(doc['id'])
    """

    directory = "data/federal/documents"
    for filename in os.listdir(directory):
        #Open the file
        with open(os.path.join(directory, filename), 'r') as file:
            # Load the JSON data as a dictionary
            data = json.load(file)
            # Split date from filename
            date = filename.split('_')[0]
            
            # Loop through each document in the data
            for doc in data['data']:
                doc_id = doc['id']
                for attribute in doc['attributes']:
                    document = {
                        "doc_id": doc_id,
                        "postedDate": doc['attributes']['postedDate'],
                        "agencyId": doc['attributes']['agencyId'],
                        "fileDate": date
                    }
                # Append the document to the list
                documents.append(document)

    df = pd.DataFrame(documents)
    return df

"""
df = get_summaries()
print(df.head())  
print(df.shape[0])
"""