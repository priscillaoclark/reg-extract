import os
from PyPDF2 import PdfReader

path = '/Users/bluebird/develop/reg_extract/data/enforcement_actions/documents/fdic/'
# Pull list of files in path
files = os.listdir(path)
# Limit to first 1 file
files = files[:1]

# Create an empty dictionary for the AI summaries with three fields
ai_summaries = {'file_name': [], 'short_summary': [], 'long_summary': []}

# Open each file and extract text with PyPDF2
for file in files:
    filename = os.path.join(path, file)
    reader = PdfReader(filename)
    count = len(reader.pages)
    print(count)
    output = []
    for i in range(count):
        page = reader.pages[i]
        output.append(page.extract_text())
    combined = ','.join(output)
    print(len(combined))
    print(file)
    print(combined)


