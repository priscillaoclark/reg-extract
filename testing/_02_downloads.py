import os
import pandas as pd

def get_downloads():
    # Create a list to store the data
    files = []

    # Loop through all .txt files located in the data/federal/logs directory
    directory = "data/federal/attachments"
    for filename in os.listdir(directory):
        file = {
            "filename": filename,
            "size": os.path.getsize(os.path.join(directory, filename)),
            "extension": os.path.splitext(filename)[1],
            "doc_id": filename.split('.')[0]
        }
        
        # Check if the document already exists in the list
        if file not in files:
            files.append(file)
            
    # Convert to a DataFrame
    df = pd.DataFrame(files)
    
    return df

"""
df = get_downloads()
print(df.head())
print(df.shape[0])
"""