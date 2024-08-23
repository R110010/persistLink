# create a .txt file named "PersistURL.txt" in working directory
# the code uploads the files to the specified url, appends the PersistURL to the text file and give a count of files written in the text file.
# Script written BY "Raj Deep Bania" on 20/11/2023
# modified on 12/01/2024. (version 3) Uploaded files moved to seperate folder one at a time for handling recovery.
# modified on 12/01/2024. (version 4) accessd url from json in single step.

import os
import requests
import json
import shutil

# Specify the URL and headers
url = "replace with your url"
headers = {}

# Specify the folder path containing the files 
folder_path = "replace with path to your folder"

# Specify the folder path containing the output folder
output_folder_path = "replace with path to your folder"
# Specify the folder for the files to ke moved after persist creation
output_folder_Files = "replace with path to your folder"


# Function to determine content type based on file extension
def get_content_type(file_name):
    if file_name.lower().endswith(('.jpg', '.jpeg')):
        return 'image/jpeg'
    elif file_name.lower().endswith('.png'):
        return 'image/png'
    elif file_name.lower().endswith('.pdf'):
        return 'application/pdf'
    # Add more file types as needed
    else:
        return 'application/octet-stream'  # Default content type for unknown file types

# List all the files in the folder
file_list = os.listdir(folder_path)

count_URL = 0  # to keep a count of the PersistURL written in the file.
# Iterate through the files and upload each one
for file_name in file_list:
    # Create file path by joining folder path and file name.
    file_path = os.path.join(folder_path,file_name)

    with open(file_path, 'rb') as file:
        content_type = get_content_type(file_name)
        if content_type == 'image/jpeg':
            content_type = 'image/jpeg'  # Set the correct content type for .jpeg files
        files = [('file', (file_name, file, content_type))]
        payload = {'ttl': '1 year'}  # validity of the PersistURL
        response = requests.post(url, headers=headers, data=payload, files=files)
        # Convert the response into text (json file) and convert the JSON to a Python object
        responseData = json.loads(response.text)  # responseData is a Dictionary

        # Extract the value of the property "file" and subproperty "directURL"
        jsonData = responseData["file"] ["directURL"]  # jsonData is a Dictionary       
        print("Writing " + jsonData)
        # Write the URL into a text file.
        with open((output_folder_path + "PersistURL.txt"), 'a') as f:  # creates a .txt file and appends the PersistURL
            f.write(jsonData + "\n")
            f.close()
            count_URL = count_URL + 1
            print(count_URL)
    
    shutil.move(file_path, output_folder_Files)

print("Total number of PersistURLs written in the text file is " + str(count_URL))