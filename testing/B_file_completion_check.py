from _04_mongodb_files import get_attachments
from _02_downloads import get_downloads
import pandas as pd
import requests

attachments = get_attachments()
downloads = get_downloads()

# Print the first 5 rows of each DataFrame
# print(attachments.head())
# print(downloads.head())

# Count the number of unique doc_ids in the attachments and downloads DataFrames
unique_attachments = attachments['doc_id'].nunique()
unique_downloads = downloads['doc_id'].nunique()
print(unique_attachments)
print(unique_downloads)

# See which doc_ids are in the attachments DataFrame but not in the downloads DataFrame
merged = pd.merge(attachments, downloads, on='doc_id', how='left', indicator=True)
missing = merged[merged['_merge'] == 'left_only']
print(missing.head())
print(missing.shape[0])

# Create a list of fileUrls for the missing documents where fileType is 'htm'
missing_htm = missing[missing['fileType'] == 'htm']
fileUrls_htm = missing_htm['fileUrl'].tolist()
print(fileUrls_htm)

# Loop through the fileUrls_htm list and download the files
for fileUrl in fileUrls_htm:
    #Strip out doc_id from fileUrl and remove the extension
    doc_id = fileUrl.split('/')[-2]
    print("Downloading file for doc_id: ", doc_id)
    response = requests.get(fileUrl)
    with open(f"data/federal/attachments/{doc_id}.htm", 'wb') as f:
        f.write(response.content)

# Check again for missing files
downloads = get_downloads()
merged = pd.merge(attachments, downloads, on='doc_id', how='left', indicator=True)
missing = merged[merged['_merge'] == 'left_only']
print(missing.head())
print(missing.shape[0])

# Fix PDF files
missing_pdf = missing[missing['fileType'] == 'pdf']
fileUrls_pdf = missing_pdf['fileUrl'].tolist()
# Ensure list is distinct
fileUrls_pdf = list(set(fileUrls_pdf))
#print(fileUrls_pdf)

# Loop through the fileUrls_pdf list and download the files
for fileUrl in fileUrls_pdf:
    #Strip out doc_id from fileUrl and remove the extension
    doc_id = fileUrl.split('/')[-2]
    print("Downloading file for doc_id: ", doc_id)
    response = requests.get(fileUrl)
    with open(f"data/federal/attachments/{doc_id}.pdf", 'wb') as f:
        f.write(response.content)

# Check again for missing files
downloads = get_downloads()
merged = pd.merge(attachments, downloads, on='doc_id', how='left', indicator=True)
missing = merged[merged['_merge'] == 'left_only']
print(missing.head())
print(missing.shape[0])

# Do the same for docx files
missing_docx = missing[missing['fileType'] == 'docx']
fileUrls_docx = missing_docx['fileUrl'].tolist()
# Ensure list is distinct
fileUrls_docx = list(set(fileUrls_docx))
#print(fileUrls_docx)

# Loop through the fileUrls_docx list and download the files
for fileUrl in fileUrls_docx:
    #Strip out doc_id from fileUrl and remove the extension
    doc_id = fileUrl.split('/')[-2]
    print("Downloading file for doc_id: ", doc_id)
    response = requests.get(fileUrl)
    with open(f"data/federal/attachments/{doc_id}.docx", 'wb') as f:
        f.write(response.content)

# Check again for missing files
downloads = get_downloads()
merged = pd.merge(attachments, downloads, on='doc_id', how='left', indicator=True)
missing = merged[merged['_merge'] == 'left_only']
print(missing.head())
print(missing.shape[0])