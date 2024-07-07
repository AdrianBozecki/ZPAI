from minio import Minio

class MinioClient:
    def __init__(self):
        self.client = Minio(
            "minio:9000",
            access_key="minio",
            secret_key="minio123",
            secure=False
        )

    def upload_file(self, bucket_name: str, object_name: str, file_path: str):
        result = self.client.fput_object(bucket_name, object_name, file_path)
        return result

    def download_file(self, bucket_name: str, object_name: str, file_path: str):
        self.client.fget_object(bucket_name, object_name, file_path)