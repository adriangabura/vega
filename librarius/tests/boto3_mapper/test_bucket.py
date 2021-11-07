import pytest
from librarius.adapters import boto_mapper


def test_delete_bucket(default_test_bucket, boto3_default_resource, boto3_default_client):
    default_test_bucket.delete()
    retrieve_result = boto_mapper.BucketOperation.get(
        boto3_default_resource, boto3_default_client, default_test_bucket.name)
    assert not retrieve_result


def test_delete_object(default_test_object, boto3_default_resource):
    default_test_object.delete()
    retrieve_result = boto_mapper.ObjectOperation.check_object_exists(
        boto3_default_resource,
        default_test_object.Bucket().name,
        default_test_object.key
    )
    assert not retrieve_result
