import ibm_boto3
import logging
from ibm_botocore.client import Config
from pathlib import Path
from typing import BinaryIO


class CosInterface:
    def __init__(self, api_key, service_instance_id, bucket_name, region, endpoint_suffix="cloud-object-storage.appdomain.cloud"):
        self.api_key = api_key
        self.service_instance_id = service_instance_id
        self.bucket_name = bucket_name
        self.region = region
        self.endpoint_url = f"https://s3.{region}.{endpoint_suffix}"

        self.cos = ibm_boto3.client(
            "s3",
            ibm_api_key_id=self.api_key,
            ibm_service_instance_id=self.service_instance_id,
            config=Config(signature_version="oauth"),
            endpoint_url=self.endpoint_url
        )

    def upload_file(self, local_path, remote_path, make_public=True):
        try:
            self.cos.upload_file(
                Filename=str(local_path),
                Bucket=self.bucket_name,
                Key=remote_path
            )

            if make_public:
                self.cos.put_object_acl(
                    Bucket=self.bucket_name,
                    Key=remote_path,
                    ACL='public-read'
                )

            public_url = f"{self.endpoint_url}/{self.bucket_name}/{remote_path}"
            return {
                "success": True,
                "url": public_url
            }

        except Exception as e:
            logging.exception("Failed to upload to IBM COS")
            return {
                "success": False,
                "error": str(e)
            }


    def upload_fileobj(self, file_obj: BinaryIO, remote_path: str, make_public=True):
        try:
            self.cos.upload_fileobj(
                Fileobj=file_obj,
                Bucket=self.bucket_name,
                Key=remote_path
            )

            if make_public:
                self.cos.put_object_acl(
                    Bucket=self.bucket_name,
                    Key=remote_path,
                    ACL='public-read'
                )

            public_url = f"{self.endpoint_url}/{self.bucket_name}/{remote_path}"
            return {
                "success": True,
                "url": public_url
            }

        except Exception as e:
            logging.exception("Failed to upload file object to IBM COS")
            return {
                "success": False,
                "error": str(e)
            }
