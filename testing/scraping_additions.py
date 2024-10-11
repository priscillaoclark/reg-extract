from _05_mongodb_attachments import get_mongodb_attachments
import pandas as pd
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
import re
from string import punctuation

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Ensure you have the NLTK data downloaded
nltk.download('punkt')
nltk.download('punkt_tab')

# Load to dataframe
mongodb = get_mongodb_attachments()

"""
# Create df with unique doc_summary values
unique_summaries = mongodb['doc_summary'].unique()
# Sort df by length of doc_summary shortest first
unique_summaries = sorted(unique_summaries, key=len)
# Print the first 5 unique doc_summary values
print(unique_summaries[:5])
"""
# Filter for documents where doc_summary equals Not Found
missing = mongodb[mongodb['doc_summary'] == 'Not found']
print(missing.shape[0])
#print(missing.columns)

# Filter for htm files
missing = missing[missing['extension'] == '.htm']
# Sort by the length of the file
missing = missing.sort_values(by='num_words', ascending=False)

"""
# Find the file name of the attachment
filename = missing['filename'].iloc[0]

# Open the file and read the contents
with open(f'{filename}', 'r') as f:
    contents = f.read()

# Count the number of times a search term appears in the document
search_term = 'summary'
count = contents.lower().count(search_term)
print(count)

# See the text around the first occurrence of the search term
index = contents.lower().find(search_term)
print(contents[index-100:index+100])
"""

# Loop through the dataframe and add the doc_ids for all documents that contain the search term
search_term = 'summary'
doc_ids = []
for index, row in missing.iterrows():
    with open(row['filename'], 'r') as f:
        contents = f.read()
        if search_term in contents:
            doc_ids.append(row['doc_id'])
            
# Print the length of the list
print(len(doc_ids))

# List to store the tokenized content
tokenized_contents = []

def preprocess_text(text):
    text = text.lower()  # Lowercase text
    text = re.sub(f"[{re.escape(punctuation)}]", "", text)  # Remove punctuation
    text = " ".join(text.split())  # Remove extra spaces, tabs, and new lines
    return text

# Iterate through the 'missing' dataframe
for index, row in missing.iterrows():
    with open(row['filename'], 'r') as f:
        contents = f.read(1000)  # Read the first 10,000 characters
        # Remove html tags
        contents = BeautifulSoup(contents, 'html.parser').get_text()
        # Preprocess the text
        contents = preprocess_text(contents)
        # Tokenize the content
        tokens = word_tokenize(contents)  # Tokenize the content
        
        # Cleaning the tokens
        # Remove punctuation from the tokens
        tokens = [token for token in tokens if token.isalnum()]
        # Remove numbers from the tokens
        tokens = [token for token in tokens if not token.isdigit()]
        # Convert the tokens to lowercase
        tokens = [token.lower() for token in tokens]
        # Remove stopwords from the tokens
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        # Remove words with less than 3 characters
        tokens = [token for token in tokens if len(token) > 2]
        # Lemmatize the tokens
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        
        # Add tokens plus the doc_id to the list
        #tokenized_contents.append((row['doc_id'], tokens))
        tokenized_contents.append(tokens)

# Print the first tokenized content as an example
print(tokenized_contents[0:1])
