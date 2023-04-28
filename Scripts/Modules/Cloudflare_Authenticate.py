import os

from boto3 import client
from botocore.config import Config
from dotenv import load_dotenv

def get_cloudflare_client():
    load_dotenv()
    return client('s3',
        endpoint_url = f"https://{os.getenv('R2_ENDPOINT')}.r2.cloudflarestorage.com",
        aws_access_key_id = os.getenv('R2_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('R2_SECRET_ACCESS_KEY'),
        config = Config(signature_version = 'v4')
    )
