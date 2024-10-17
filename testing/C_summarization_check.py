from _05_mongodb_attachments import get_mongodb_attachments
from _03_mongodb import get_documents
from _02_downloads import get_downloads
import pandas as pd
from parse_doc import summarize_attachments
import os

mongodb = get_mongodb_attachments()
documents = get_documents()
downloads = get_downloads()

#print(mongodb.head())  # attachments loaded into mongodb
#print(documents.head())
#print(downloads.head())

# Check 1
# Merge the two DataFrames and show which documents are not in the mongodb DataFrame
merged = pd.merge(downloads, mongodb, on='doc_id', how='left', indicator=True)
missing = merged[merged['_merge'] == 'left_only']

# Join missing to documents to get the metadata and sort by posted date to see the newest documents
missing = pd.merge(missing, documents, on='doc_id', how='inner')
missing = missing.sort_values(by='postedDate', ascending=False)

# Filter by htm files
missing = missing[missing['extension_x'] == '.htm']

# Show just the document ID and posted date
print(missing[['doc_id', 'postedDate','filename_x']])
print(missing.shape[0])
##print(missing.columns)
# 1326

# Problem documents to review later
missing = missing[missing['doc_id'] != 'NCUA-2024-0054-0001']
missing = missing[missing['doc_id'] != 'NCUA-2024-0053-0001']
missing = missing[missing['doc_id'] != 'FINCEN-2024-0006-0056']
missing = missing[missing['doc_id'] != 'FINCEN-2024-0006-0055']

def process(data):
    directory = "data/federal/attachments"
    # Pick 20 htm files and process them through the summarization function
    #htm_files = files[files['fileType'] == 'htm']
    #to_process = data.head(150)
    to_process = data
    for index, row in to_process.iterrows():
        print(f"Processing document {row['doc_id']}")
        # Join the directory and filename to get the full path
        path = os.path.join(directory, row['filename_x'])
        summarize_attachments(path)

process(missing)

"""
# Check 2
# Show the records in mongodb that are missing an ai_summary_short
missing_ai_summary = mongodb[mongodb['ai_summary_short'].isnull()]
if missing_ai_summary.shape[0] > 0:
    print(missing_ai_summary['doc_id'].values)
else:
    print("No missing ai_summary_short records found.")
"""


