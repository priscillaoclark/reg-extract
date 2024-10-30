import os
import requests
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from _03_mongodb import get_documents
import datetime
from _05_mongodb_attachments import get_mongodb_attachments

# Example usage
df = get_mongodb_attachments()
# Count the number of documents
#print(df.shape[0])
# Clean up doc ID column - pull the ID from the URL
df['doc_id'] = df['doc_id'].str.split('/').str[-1]
#print(df.head())

# Bring in document metadata
metadata = get_documents()
metadata_df = pd.DataFrame(metadata)

# Merge the two dataframes on the doc_id column
df_combined = pd.merge(df, metadata_df, on='doc_id', how='inner')
#print(df_combined.head())
#print(df_combined.columns)

# Count the number of documents
print(df_combined.shape[0])

# Filter for documents posted yesterday
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')
df_combined = df_combined[df_combined['postedDate'] == yesterday_str]

# Print the doc_id and ai_summary_short for each document
for index, row in df_combined.iterrows():
    print(f"""Doc ID: {row['doc_id']}\n
          Date Posted: {row['postedDate']}\n
          Title: {row['title_y']}\n
          Agency: {row['agency']}\n
          Document Type: {row['documentType']}\n
          AI Summary: {row['ai_summary_short']}\n
          Document Summary: {row['doc_summary']}\n
          --------------------------------------------------\n
          """)