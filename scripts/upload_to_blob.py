import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Retrieve the connection string from environment variables
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Specify the container name
container_name = os.getenv('CONTAINER_NAME')

# Directory containing the JSON files
data_dir = Path("data") / "raw"

def upload_to_blob(container_name, blob_name, file_path):
    try:
        # Get a reference to the container
        container_client = blob_service_client.get_container_client(container_name)

        # Get a reference to the blob
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload the file
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"File {file_path} uploaded to {container_name}/{blob_name}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Upload all JSON files in the data/raw directory
for file_path in data_dir.glob("*.json"):
    upload_to_blob(container_name, file_path.name, file_path)
