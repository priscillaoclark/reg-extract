from _03_mongodb import get_documents
from _04_mongodb_files import get_attachments
from datetime import datetime, timedelta

documents = get_documents()
attachments = get_attachments()

# Show records where the posted date is yesterday
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')
documents = documents[documents['postedDate'] == yesterday_str]
attachments = attachments[attachments['postedDate'] == yesterday_str]