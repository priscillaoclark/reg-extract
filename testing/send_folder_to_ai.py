import sys
sys.path.insert(0, '/Users/bluebird/develop/reg_extract/')
from testing.llm_summary import get_ai_summaries
import os
from PyPDF2 import PdfReader

def folder_to_ai(path):
    
    # Pull list of files in path
    files = os.listdir(path)
    
    # Create an empty dictionary for the AI summaries with three fields
    ai_summaries = {'file_name': [], 'short_summary': [], 'long_summary': []}
    
    # Open each file and extract text
    for file in files:
        filename = os.path.join(path, file)
        try: 
            reader = PdfReader(filename)
            count = len(reader.pages)
            print(count)
            output = []
            for i in range(count):
                page = reader.pages[i]
                output.append(page.extract_text())
                combined = ','.join(output)
                try:
                    ai_summary = get_ai_summaries(combined)
                    ai_summary_short, ai_summary_long = ai_summary
                
                    # Add the file name and summaries to the dictionary
                    ai_summaries['file_name'].append(file)
                    ai_summaries['short_summary'].append(ai_summary_short)
                    ai_summaries['long_summary'].append(ai_summary_long)
                except Exception as e:
                    print(f"Error generating AI summaries for {file}: {e}")
        except Exception as e:
            print(f"Error reading file {file}: {e}")
            
    return ai_summaries
    
"""
# example usage
path = '/Users/bluebird/develop/reg_extract/data/enforcement_actions/documents/fdic'
summaries = link_to_ai(path)
print(summaries)
"""