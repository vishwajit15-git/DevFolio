import os
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "devfolio")
GCS_PROJECT_ID = os.getenv("GCS_PROJECT_ID")
# This should be the path to the downloaded service account JSON file
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

def get_gcs_client() -> storage.Client:
    if not GOOGLE_APPLICATION_CREDENTIALS or not os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set or file does not exist.")
    
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    return storage.Client(credentials=credentials, project=GCS_PROJECT_ID)

def upload_file_to_gcs(local_file_path: str, destination_blob_name: str) -> str:
    """
    Uploads a local file to the Google Cloud Storage bucket.
    Returns the public URL of the uploaded object.
    """
    client = get_gcs_client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    
    # Upload the file
    blob.upload_from_filename(local_file_path, content_type="image/png")
    
    # Return the public URL
    return f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{destination_blob_name}"
