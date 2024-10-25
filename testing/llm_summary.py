import os
import json
import pandas as pd
import openai
import time
from dotenv import load_dotenv
import re

def summarize_with_assistant(assistant_id, text_to_summarize, api_key):
    client = openai.Client(api_key=api_key)
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Please summarize the following text:\n\n{text_to_summarize}"
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    start_time = time.time()
    timeout = 300  # 5 minutes timeout
    while run.status not in ["completed", "failed"]:
        if time.time() - start_time > timeout:
            print(f"Run timed out after {timeout} seconds")
            return None
        print("Waiting 45 seconds to prevent rate limiting...")  # tokens per min (TPM): Limit 30000
        time.sleep(45)  # Increase sleep time to reduce API calls
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Current run status: {run.status}")  # Debug print

    if run.status == "failed":
        print(f"Run failed. Error: {run.last_error.message}")
        return None

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    summary = messages.data[0].content[0].text.value
    return summary

def get_ai_summaries(data, assistant_id):
        
        # Clear existing environment variables
        for key in list(os.environ.keys()):
            if key.startswith("OPENAI"):
                del os.environ[key]
                
        # Get the API key from the .env file
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        
        # Remove any HTML tags
        data = re.sub(r'<[^>]*>', '', data)
        # Clean up the text by removing extra spaces and newlines
        text_to_summarize = ' '.join(data.split())
        
        # For testing, cut the text to 75000 characters
        # text_to_summarize = text_to_summarize[:75000]
        
        # Handle context window limits
        character_limit = 100000
        # Split the text into chunks of characters
        print(f"Creating chunks from {len(text_to_summarize)} length text.")
        text_chunks = [text_to_summarize[i:i + character_limit] for i in range(0, len(text_to_summarize), character_limit)]
        
        # Create an empty json for the summaries
        summaries = []
        
        # Loop through each chunk and summarize it
        for i, chunk in enumerate(text_chunks):
            try:
                print(f"Summarizing chunk {i+1} of {len(text_chunks)} ({len(chunk)} characters)")
                summary = summarize_with_assistant(assistant_id, chunk, OPENAI_API_KEY)
                if summary is None:
                    print(f"Failed to summarize chunk {i+1}")
                    continue
                summaries.append(summary)
                print(f"Finished summarizing chunk {i+1}")
            except Exception as e:
                print(f"Error summarizing chunk {i+1}: {e}")
                continue
        
        # If multiple summaries were created, join them into a single string and summarize again
        if len(summaries) > 1:
            # Create a joined string of all the summaries
            joined_summaries = '\n'.join(summaries)
            # Trim the joined string to character limit
            joined_summaries = joined_summaries[:character_limit]

            # Feed the summary list back to the assistant to summarize the summaries
            try:
                print(f"Creating summary of summaries from {len(joined_summaries)} length text.")
                summary_of_summaries = summarize_with_assistant(assistant_id, joined_summaries, OPENAI_API_KEY)
                if summary_of_summaries is None:
                    print("Failed to create summary of summaries")
            except Exception as e:
                print(f"Error summarizing summaries: {e}")
                return summaries, None
        else:
            summary_of_summaries = summaries[0]
            
        return summary_of_summaries, summaries

"""
# Example usage
ai_summary = get_ai_summaries()
if ai_summary:
    ai_summary_short, ai_summary_long = ai_summary
    print("Short summary:", ai_summary_short)
    print("Long summary:", ai_summary_long)
else:
    print("Failed to generate summaries")
"""
                        