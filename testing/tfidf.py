import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re

custom_stop_words = ['respondent']

def clean_text(text):
    text = re.sub(r'\d+', '', text)
    # Remove custom stop words
    for stop_word in custom_stop_words:
        text = text.replace(stop_word, '')
    text = ' '.join(text.split())
    return text

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            try:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in range(len(reader.pages)):
                    text += reader.pages[page].extract_text()
            except Exception as e:
                print(f"Error reading PDF: {pdf_path}")
                return ""
        text = clean_text(text)
    except Exception as e:
        print(f"Error extracting text from PDF: {pdf_path}")
        text = ""
    return text

def extract_text_from_html(html_path):
    try:
        with open(html_path, 'r') as f:
            try:
                text = f.read()
            except Exception as e:
                print(f"Error reading HTML: {html_path}")
                return ""
        text = clean_text(text)
    except Exception as e:
        print(f"Error extracting text from HTML: {html_path}")
        text = ""
    return text

# Paths to your PDF files
#folder = "/Users/bluebird/develop/reg_extract/data/enforcement_actions/documents/frb/"
folder = "/Users/bluebird/develop/reg_extract/data/federal/attachments/"
pdf_files = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.pdf')]
html_files = [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.htm')]
files = pdf_files + html_files

# Extract text from each PDF
documents = [extract_text_from_pdf(pdf) for pdf in pdf_files]
# Add text from HTML files
documents = [extract_text_from_html(html) for html in html_files]

# Update TF-IDF to use n-grams (e.g., unigrams, bigrams, trigrams)
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), min_df = 10, max_df=0.5)
X = vectorizer.fit_transform(documents)
keywords_per_document = np.array(vectorizer.get_feature_names_out())

# Prepare the dataframe
data = []

for i, file in enumerate(files):
    sorted_keywords_idx = np.argsort(X[i].toarray()).flatten()[::-1]  # Sort by TF-IDF score
    top_keywords = keywords_per_document[sorted_keywords_idx][:10]  # Get top 10 keywords
    top_keywords_str = ', '.join(top_keywords)  # Convert keywords list to string
    data.append([os.path.basename(file), top_keywords_str])  # Append filename and keywords to data list

# Create the dataframe
df = pd.DataFrame(data, columns=['Filename', 'Top Keywords'])
print(df)

# Save the dataframe to a CSV file
output_file = os.path.join(folder, 'tfidf_keywords.csv')
df.to_csv(output_file, index=False)



