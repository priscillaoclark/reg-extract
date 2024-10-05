import os
import pandas as pd
from bs4 import BeautifulSoup

# Create a list to store the data
files = []

# Loop through all .txt files located in the data/federal/logs directory
directory = "data/federal/attachments/testing"
for filename in os.listdir(directory):
    # Open the file
    with open(os.path.join(directory, filename), 'r') as file:
        # Read the contents of the file
        contents = file.read()
        
        
        # Strip the doc ID from the filename
        doc_id = filename.split('.')[0]
        # Get the total number of words in the document
        num_words = len(contents.split())
        # Get the total number of unique words in the document
        num_unique_words = len(set(contents.split()))
        # Get the file extension
        extension = os.path.splitext(filename)[1]
        
        # Parse the HTML content
        soup = BeautifulSoup(contents, 'html.parser')
        # Find the title of the document
        title = soup.find('title').text

        # Create a container to store the links
        links = []
        # Loop through each link
        for link in soup.find_all('a'):
            # Get the URL
            url = link.get('href')
            # Append the URL to the list
            links.append(url)
        
        # Add fields to the dictionary
        file = {
            "filename": filename,
            "doc_id": doc_id,
            "doc_size": os.path.getsize(os.path.join(directory, filename)),
            "extension": extension,
            "num_words": num_words,
            "num_unique_words": num_unique_words,
            "title": title,
            "num_links": len(links),
            "links": links
        }
        # Append the document to the list
        files.append(file)

# Convert to a DataFrame
df = pd.DataFrame(files)
print(df.head)