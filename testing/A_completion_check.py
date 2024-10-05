from _01_log import get_log_counts
from _03_mongodb import get_documents
from _01_summary import get_summaries
import pandas as pd

log = get_log_counts()
documents = get_documents()
summaries = get_summaries()

# Print the first 5 rows of each DataFrame
# print(log.head())
# print(documents.head())
# print(summaries.head())

"""
# Aggregate the data in the documents dataframe by agencyId and compare to the log data
agency_counts = documents.groupby('agencyId').size().reset_index(name='Count')

# Aggregate the log data by date and acronym
log_counts = log.groupby(['Acronym']).sum().reset_index()
# Only keep the Acronym and Count columns
log_counts = log_counts[['Acronym', 'Count']]

# Merge the two DataFrames on the Acronym column
merged = pd.merge(agency_counts, log_counts, left_on='agencyId', right_on='Acronym')
print(merged.head())
"""

# Count the number of unique doc_ids in the summaries and documents DataFrames
unique_summaries = summaries['doc_id'].nunique()
unique_documents = documents['doc_id'].nunique()
print(unique_summaries)
print(unique_documents)


# Compare the doc_id from the summaries and documents DataFrames
# Merge the two DataFrames on the doc_id column and show which doc_ids are not in the documents DataFrame
merged = pd.merge(summaries, documents, on='doc_id', how='left', indicator=True)
missing = merged[merged['_merge'] == 'left_only']
print(missing.head())

# Fix missing documents
from fix_missing import upload_single_document

# For doc_id in missing, loop through and upload the document
for doc in missing['doc_id']:
    #upload_single_document(doc, 'federal_documents')
    print(doc)

# Merge the two DataFrames on the doc_id column and show which doc_ids are not in the summaries DataFrame
merged_2 = pd.merge(summaries, documents, on='doc_id', how='right', indicator=True)
missing_2 = merged_2[merged_2['_merge'] == 'right_only']
print(missing_2.shape[0])