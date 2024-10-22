from extract_federal import extract_federal
from testing._03_mongodb import get_documents
from testing.send_mongo_to_sql import send_mongo_to_sql

extract_federal()
data = get_documents()
send_mongo_to_sql(data)

