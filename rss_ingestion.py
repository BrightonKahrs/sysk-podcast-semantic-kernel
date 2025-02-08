import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Define the RSS feed URL and Azure Storage details
rss_url = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/A91018A4-EA4F-4130-BF55-AE270180C327/44710ECC-10BB-48D1-93C7-AE270180C33E/podcast.rss"

# Define the ADLS Gen2 details
adls_account_name = os.getenv("ADLS_ACCOUNT_NAME")
adls_account_key = os.getenv("ADLS_ACCOUNT_KEY")
file_system_name = os.getenv("FILE_SYSTEM_NAME")
directory_name = os.getenv("DIRECTORY_NAME")

# Generate a timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Define the file name with the timestamp
file_name = f"sysk_podcast_{timestamp}.rss"

# Create a DataLakeServiceClient
adls_service_client = DataLakeServiceClient(account_url=f"https://{adls_account_name}.dfs.core.windows.net", credential=adls_account_key)

# Get a file system client
file_system_client = adls_service_client.get_file_system_client(file_system=file_system_name)

# Get a directory client
directory_client = file_system_client.get_directory_client(directory_name)

# Get a file client
file_client = directory_client.get_file_client(file_name)

# Fetch the RSS feed content
response = requests.get(rss_url)
rss_content = response.content

# Upload the RSS feed to ADLS Gen2
file_client.upload_data(rss_content, overwrite=True)

print(f"RSS feed uploaded to Azure Data Lake Storage directory '{directory_name}' as file '{file_name}'")