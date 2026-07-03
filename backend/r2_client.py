import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

# Cloudflare R2 Settings from environment variables
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "devfolio")
# This is the public custom domain or r2.dev domain to serve the images from
R2_PUBLIC_DOMAIN = os.getenv("R2_PUBLIC_DOMAIN", "https://pub-xxxxxx.r2.dev")

def get_r2_client():
    if not R2_ACCOUNT_ID:
        raise ValueError("R2_ACCOUNT_ID is not set in the environment.")
    
    # Initialize the S3 client to point to Cloudflare R2
    s3_client = boto3.client(
        's3',
        endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )
    return s3_client

def upload_file_to_r2(local_file_path: str, object_name: str) -> str:
    """
    Uploads a local file to the Cloudflare R2 bucket.
    Returns the public URL of the uploaded object.
    """
    client = get_r2_client()
    
    # Upload the file
    client.upload_file(
        local_file_path, 
        R2_BUCKET_NAME, 
        object_name,
        ExtraArgs={"ContentType": "image/png"} # Assuming we only upload PNG screenshots
    )
    
    # Return the public URL string
    return f"{R2_PUBLIC_DOMAIN}/{object_name}"
