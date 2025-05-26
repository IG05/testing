import boto3
import os

BUCKET_NAME = "pipeline-watchai"
REGION = "us-east-1"

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=REGION
)

def upload_to_s3(file_path, key):
    # Determine content type based on file extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        content_type = "image/jpeg"
    elif ext == ".png":
        content_type = "image/png"
    elif ext == ".wav":
        content_type = "audio/wav"
    elif ext == ".mp3":
        content_type = "audio/mpeg"
    else:
        content_type = "application/octet-stream"  # default fallback
    
    s3.upload_file(file_path, BUCKET_NAME, key, ExtraArgs={'ContentType': content_type})

def generate_s3_url(key):
    return f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{key}"
