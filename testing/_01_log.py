import pandas as pd
import os

def get_log_counts():

    # Initialize an empty dictionary to store the data
    data = {'Date': [], 'Acronym': [], 'Count': []}

    # Loop through all .txt files located in the data/federal/logs directory
    directory = "data/federal/logs"
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            # Strip out the date from the file name
            date = filename.split('_')[0]

            # Read and parse the log file
            with open(file_path, 'r') as file:
                for line in file:
                    if line.strip() and '---' not in line:
                        acronym, count = line.split(':')
                        data['Date'].append(date)
                        data['Acronym'].append(acronym.strip())
                        data['Count'].append(int(count.strip()))

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)
    
    return df