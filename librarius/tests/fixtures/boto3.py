import pytest

from mypy_boto3_s3 import S3ServiceResource, S3Client
from mypy_boto3_s3.service_resource import Bucket
from boto3 import Session

from librarius.config import BasicConfig
from librarius.adapters import boto_mapper
from librarius.service_layer.dto import FileUploadDto


@pytest.fixture(scope="session")
def boto3_default_session(config) -> Session:
    return Session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION,
    )


@pytest.fixture(scope="session")
def boto3_default_resource(boto3_default_session: Session) -> S3ServiceResource:
    return boto3_default_session.resource("s3")


@pytest.fixture(scope="session")
def boto3_default_client(boto3_default_resource: S3ServiceResource) -> S3Client:
    return boto3_default_resource.meta.client


@pytest.fixture(scope="session")
def s3_mapper(boto3_default_session) -> boto_mapper.SessionWrapper:
    return boto_mapper.SessionWrapper(boto3_default_session)


@pytest.fixture(scope="session")
def file_dto() -> FileUploadDto:
    body = '<a href="https://google.com">Hello</a>'
    encoded_body = bytes(body, "utf")

    return FileUploadDto.from_body(encoded_body, "text/html")


@pytest.fixture(scope="function")
def default_test_bucket(
    boto3_default_resource: S3ServiceResource,
    boto3_default_client: S3Client,
    config: BasicConfig,
):
    bucket = boto_mapper.BucketOperation.create(
        resource=boto3_default_resource,
        name="cerbulan.burbulan",
        region=config.AWS_REGION,
    )
    yield bucket
    boto_mapper.BucketOperation.delete(
        resource=boto3_default_resource,
        client=boto3_default_client,
        name=bucket.name,
        force_empty=True,
        force_empty_with_versioning=True,
    )


@pytest.fixture(scope="function")
def default_test_object(default_test_bucket: Bucket, file_dto: FileUploadDto, boto3_default_resource: S3ServiceResource):
    test_object = boto_mapper.ObjectOperation.put(
        bucket=default_test_bucket,
        binary_content=file_dto.body,
        content_md5_hash=file_dto.content_md5_hash,
        content_type=file_dto.content_type,
        key="key.cerbulan",
    )
    yield test_object
    boto_mapper.ObjectOperation.delete(boto3_default_resource, default_test_bucket.name, "key.cerbulan")
