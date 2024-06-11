import os
from azure.storage.blob import BlobServiceClient
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up your connection to Azure Blob Storage
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_CONTAINER_NAME')
local_data_dir = Path(__file__).resolve().parent.parent / 'data' / 'raw'

def upload_all_to_blob():
    if connection_string is None or container_name is None:
        raise ValueError("Azure Storage connection string or container name is not set in environment variables.")
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Get list of JSON files in the local data directory
    json_files = sorted(local_data_dir.glob('*.json'), key=os.path.getmtime)

    if not json_files:
        print("No JSON files found to upload.")
        return

    for json_file in json_files:
        blob_client = container_client.get_blob_client(json_file.name)

        with open(json_file, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"Uploaded {json_file.name} to {container_name}.")

if __name__ == "__main__":
    upload_all_to_blob()
