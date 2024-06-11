import os
from azure.storage.blob import BlobServiceClient
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the connection string and container name from environment variables
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_CONTAINER_NAME')

# Check if the environment variables are loaded correctly
if not connection_string or not container_name:
    raise ValueError("Missing required environment variables for Azure Blob Storage.")

local_data_dir = Path(__file__).resolve().parent.parent / 'data' / 'raw'

def upload_to_blob():
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Get list of JSON files in the local data directory
    json_files = sorted(local_data_dir.glob('*.json'), key=os.path.getmtime)

    # Upload the latest file
    latest_file = json_files[-1]
    blob_client = container_client.get_blob_client(latest_file.name)

    with open(latest_file, 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"Uploaded {latest_file.name} to {container_name}.")

    # List blobs in the container and sort them by the date in their filename
    blob_list = list(container_client.list_blobs())
    blob_list.sort(key=lambda x: x.name)

    # Ensure only the most recent 5 files are kept
    if len(blob_list) > 5:
        blobs_to_delete = blob_list[:-5]
        for blob in blobs_to_delete:
            blob_client_to_delete = container_client.get_blob_client(blob.name)
            blob_client_to_delete.delete_blob()
            print(f"Deleted {blob.name} from blob storage.")

            # Also delete the corresponding local file if it exists
            local_file_to_delete = local_data_dir / blob.name
            if local_file_to_delete.exists():
                local_file_to_delete.unlink()
                print(f"Deleted {local_file_to_delete.name} from local storage.")

if __name__ == "__main__":
    upload_to_blob()