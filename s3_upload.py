import os
from dotenv import load_dotenv
import boto3

# Load environment variables
load_dotenv()

def upload_to_s3(file_path):
    """Upload a file to AWS S3."""
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    bucket_path = os.getenv("AWS_BUCKET_PATH") + os.path.basename(file_path)
    
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        s3.upload_file(file_path, bucket_name, bucket_path)
        print(f"File uploaded successfully to s3://{bucket_name}/{bucket_path}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

if __name__ == "__main__":
    file_to_upload = "data/postgres_backup.sql"
    upload_to_s3(file_to_upload)
