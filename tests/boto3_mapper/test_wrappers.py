import pytest
from librarius.adapters import boto_mapper


def test_bucket_wrapper_upload_file(
    boto3_default_resource, default_test_bucket, boto3_default_session, file_dto
):
    bucket_wrapper = boto_mapper.BucketWrapper(
        boto3_default_session,
        default_test_bucket.name,
    )
    file_key = "cerbulan.adrian.testan"
    file = bucket_wrapper.upload_file(file_dto, file_key)
    retrieved_file = boto_mapper.ObjectOperation.retrieve(
        boto3_default_resource, default_test_bucket.name, file_key
    )
    assert file == retrieved_file
    boto_mapper.ObjectOperation.delete(
        boto3_default_resource, default_test_bucket.name, file_key
    )


def test_bucket_wrapper_delete_file(
    default_test_bucket, boto3_default_session, file_dto
):
    bucket_wrapper = boto_mapper.BucketWrapper(
        boto3_default_session,
        default_test_bucket.name,
    )
    file_key = "cerbulan.adrian.testan"
    boto_mapper.ObjectOperation.put(
        bucket=default_test_bucket,
        binary_content=file_dto.body,
        content_md5_hash=file_dto.content_md5_hash,
        content_type=file_dto.content_type,
        key=file_key,
    )
    result = bucket_wrapper.delete_file(file_key)
    assert result
