import os
import logging
from minio import Minio
from minio.error import S3Error
import uuid

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MINIO_URL = os.getenv("MINIO_URL", "s3.local:9002")
MINIO_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minio")
MINIO_SECRET_KEY = os.getenv("AWS_ACCESS_KEY", "minio123")
BUCKET_NAME = "meals"

logger.info(f"Connecting to MinIO at {MINIO_URL} with access key {MINIO_ACCESS_KEY}")

client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def upload_image(file):
    try:
        if not client.bucket_exists(BUCKET_NAME):
            logger.info(f"Bucket {BUCKET_NAME} does not exist. Creating bucket.")
            client.make_bucket(BUCKET_NAME)
        else:
            logger.info(f"Bucket {BUCKET_NAME} already exists.")

        file_id = str(uuid.uuid4())
        file_name = f"{file_id}.jpg"

        logger.info(f"Uploading file {file_name} to bucket {BUCKET_NAME}")

        client.put_object(
            BUCKET_NAME,
            file_name,
            file,
            length=-1,
            part_size=10 * 1024 * 1024,
            content_type="image/jpeg"
        )
        url = f"http://{MINIO_URL}/{BUCKET_NAME}/{file_name}"
        logger.info(f"File uploaded successfully. URL: {url}")
        return url
    except S3Error as e:
        logger.error("Error occurred while uploading file.", exc_info=True)
        return None