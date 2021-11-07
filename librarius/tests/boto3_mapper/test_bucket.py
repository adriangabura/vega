import pytest
from librarius.adapters import boto_mapper


def test_delete_bucket(default_test_bucket, boto3_default_resource, boto3_default_client):
    default_test_bucket.delete()
    retrieve_result = boto_mapper.BucketOperation.get(
        boto3_default_resource, boto3_default_client, default_test_bucket.name)
    assert retrieve_result == False
