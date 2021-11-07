import typing as tp
import logging

from mypy_boto3_s3 import S3Client, S3ServiceResource
from mypy_boto3_s3.service_resource import Bucket, Object

from boto3 import Session
from botocore.client import BaseClient
from boto3.exceptions import ResourceNotExistsError
from botocore.exceptions import ClientError

from librarius.config.utils import TRegions
from librarius.service_layer.dto import FileUploadDto

logger = logging.getLogger(__name__)


class S3File:
    pass


class BucketOperation:
    """BucketOperations contains the main operations done on buckets like create, delete, retrieve, empty, count objects"""

    @staticmethod
    def create(
        resource: S3ServiceResource, name: str, region: TRegions
    ) -> tp.Union[Bucket, tp.Literal[False]]:
        """Create an S3 bucket"""

        try:
            bucket = resource.Bucket(name)
            bucket_kwargs: dict = {
                "CreateBucketConfiguration": {"LocationConstraint": region}
            }
            response = bucket.create(**bucket_kwargs)
            status_code = response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code == 200:
                logger.info(f"Created bucket {name} at region {region}.")
            return bucket
        except ClientError as error:
            status_code = error.response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code == 409:
                logger.error(
                    f"""Bucket '{name}' already owned by you in region 
                    '{error.response['ResponseMetadata']['HTTPHeaders']['x-amz-bucket-region']}'."""
                )
            elif error.response["Error"]["Code"] == "InvalidBucketName":
                logger.error(f"Creating a bucket with with name '{name}' failed because the name is invalid.")
            else:
                logger.exception(error.response)
            return False

    @staticmethod
    def get(
        resource: S3ServiceResource, client: S3Client, name: str
    ) -> tp.Union[Bucket, tp.Literal[False]]:
        """Get an S3 bucket instance"""
        bucket = resource.Bucket(name)
        if client is not None:
            try:
                client.head_bucket(Bucket=bucket.name)
            except ClientError as error:
                status_code = error.response["ResponseMetadata"]["HTTPStatusCode"]
                if status_code == 404:
                    logger.error(f"Bucket '{name}' not found.")
                else:
                    logger.exception(error)
                return False
            else:
                return bucket

    @staticmethod
    def get_or_create(
        resource: S3ServiceResource, client: S3Client, name: str, region: TRegions
    ) -> Bucket:
        """Get an S3 bucket instance or create an S3 bucket"""
        if client is not None:
            bucket = BucketOperation.get(resource, client, name)
            if bucket:
                return bucket
            else:
                return BucketOperation.create(resource, name, region)

    @staticmethod
    def empty(
        resource: S3ServiceResource,
        client: S3Client,
        name: str,
        versioning: bool = False,
    ):
        """Empty an S3 bucket"""
        try:
            bucket = BucketOperation.get(resource, client, name)
            bucket_versioning = resource.BucketVersioning(name)
            if bucket_versioning.status == "Enabled" and versioning:
                bucket.object_versions.delete()
                return True
            elif bucket_versioning.status == "Disabled" and not versioning:
                bucket.objects.all().delete()
                return True
        except ClientError as error:
            logger.error(error)
            return False

    @staticmethod
    def delete(
        resource: S3ServiceResource,
        client: S3Client,
        name: str,
        force_empty: bool = False,
        force_empty_with_versioning: bool = False,
    ) -> bool:
        """Delete an S3 bucket"""
        bucket = BucketOperation.get(resource, client, name)
        if bucket:
            try:
                if force_empty:
                    BucketOperation.empty(
                        resource, client, name, force_empty_with_versioning
                    )
                bucket.delete()
            except ClientError as error:
                status_code = error.response["ResponseMetadata"]["HTTPStatusCode"]
                if status_code == 409:
                    logger.error(
                        f"The bucket '{name}' that you tried to delete is not empty."
                    )
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def count_objects(resource: S3ServiceResource, client: S3Client, name: str) -> int:
        bucket = BucketOperation.get(resource, client, name)
        return sum(1 for _ in bucket.objects.all())


class ObjectOperation:
    @staticmethod
    def retrieve(
        resource: S3ServiceResource, bucket_name: str, key: str
    ) -> tp.Union[Object, tp.Literal[False]]:
        try:
            return resource.Object(bucket_name, key)
        except ClientError as error:
            logger.exception(error)

    @staticmethod
    def delete(resource: S3ServiceResource, bucket_name: str, key: str) -> bool:
        try:
            s3_object = ObjectOperation.retrieve(resource, bucket_name, key)
            result = s3_object.delete()
            return True
        except ClientError as error:
            logger.exception(error)
            return False

    @staticmethod
    def put(
        bucket: Bucket,
        binary_content,
        content_md5_hash,
        content_type,
        key,
    ) -> tp.Union[Object, tp.Literal[False]]:
        try:
            return bucket.put_object(
                Body=binary_content,
                ContentMD5=content_md5_hash,
                ContentType=content_type,
                Key=key,
            )
        except ClientError as error:
            status_code = error.response["ResponseMetadata"]["HTTPStatusCode"]
            if status_code == 400:
                logger.error(error.response)
            else:
                logger.exception(error.response)
            return False

    @staticmethod
    def check_object_exists(
        resource: S3ServiceResource, bucket_name: str, key: str
    ) -> bool:
        try:
            resource.Object(bucket_name, key).load()
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                return False
        else:
            return True

    @staticmethod
    def generate_presigned_url(
        resource: S3ServiceResource, client: S3Client, bucket_name: str, key: str
    ) -> tp.Union[str, tp.Literal[False]]:
        if not ObjectOperation.check_object_exists(resource, bucket_name, key):
            return False
        try:
            response = client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": key},
                ExpiresIn=config.PRESIGNED_URL_EXPIRATION,
            )
        except ClientError as error:
            logger.error(error.response)
            return False
        else:
            return response


class BucketWrapper:
    """BucketWrapper only uses BucketOperations and ObjectOperations to upload and delete files and create and clean-up buckets"""

    def __init__(
        self, resource: S3ServiceResource, bucket_name: str, region_name: TRegions
    ):
        self._resource = resource
        self._client = resource.meta.client
        self.bucket_name = bucket_name
        self.region_name = region_name

    def upload_file(self, file_dto: FileUploadDto, key: str):
        bucket = BucketOperation.get_or_create(
            resource=self._resource,
            client=self._client,
            name=self.bucket_name,
            region=self.region_name,
        )
        result = ObjectOperation.put(
            bucket=bucket,
            binary_content=file_dto.body,
            content_md5_hash=file_dto.content_md5_hash,
            content_type=file_dto.content_type,
            key=key,
        )
        return result

    def delete_file(self, key: str):
        bucket = BucketOperation.get(self._resource, self._client, self.bucket_name)
        if bucket:
            result = ObjectOperation.delete(self._resource, self.bucket_name, key)
            count = BucketOperation.count_objects(
                self._resource, self._client, self.bucket_name
            )
            if not count:
                result = BucketOperation.delete(
                    self._resource, self._client, self.bucket_name
                )


class SessionWrapper:
    def __init__(self, session: Session):
        self.session = session
        self.resource = session.resource("s3")
        self.client = self.resource.meta.client
        self.buckets: dict = dict()

    def initialize_bucket_wrapper(self, bucket_name: str) -> BucketWrapper:
        self.buckets[bucket_name] = BucketWrapper(
            self.resource, bucket_name, self.session.region_name
        )
        return self.buckets[bucket_name]

    @classmethod
    def from_config(
        cls,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: TRegions,
    ):
        session = Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        return cls(
            session,
        )


class FileRepository:
    def upload_file(self):
        pass

    def delete_file(self):
        pass

    def find_file(self):
        pass
