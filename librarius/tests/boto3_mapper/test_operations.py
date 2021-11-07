import pytest
from librarius.adapters import boto_mapper


def test_get_bucket(default_test_bucket, boto3_default_resource, boto3_default_client):
    bucket = boto_mapper.BucketOperation.get(
        boto3_default_resource, boto3_default_client, default_test_bucket.name
    )
    assert bucket.name == default_test_bucket.name


def test_get_or_create_bucket(
    boto3_default_resource, boto3_default_client, boto3_default_session
):
    bucket_name = "ffewgrrthtrrhrthrthrthrth"
    bucket = boto_mapper.BucketOperation.get_or_create(
        boto3_default_resource,
        boto3_default_client,
        bucket_name,
        boto3_default_session.region_name,
    )
    assert bucket.name == bucket_name
    bucket.delete()


def test_delete_bucket(
    default_test_bucket, boto3_default_resource, boto3_default_client
):
    default_test_bucket.delete()
    retrieve_result = boto_mapper.BucketOperation.get(
        boto3_default_resource, boto3_default_client, default_test_bucket.name
    )
    assert not retrieve_result


def test_delete_object(default_test_object, boto3_default_resource):
    default_test_object.delete()
    retrieve_result = boto_mapper.ObjectOperation.check_object_exists(
        boto3_default_resource,
        default_test_object.Bucket().name,
        default_test_object.key,
    )
    assert not retrieve_result


def test_create_and_teardown_bucket(
    boto3_default_resource, boto3_default_session, boto3_default_client
):
    bucket_name = "frgrgergregergergerhryjrt"
    boto_mapper.BucketOperation.create(
        resource=boto3_default_resource,
        name=bucket_name,
        region=boto3_default_session.region_name,
    )

    bucket = boto_mapper.BucketOperation.get(
        boto3_default_resource, boto3_default_client, bucket_name
    )
    assert bucket.name == bucket_name

    boto_mapper.BucketOperation.delete(
        boto3_default_resource, boto3_default_client, bucket_name
    )
    bucket = boto_mapper.BucketOperation.get(
        boto3_default_resource, boto3_default_client, bucket_name
    )
    assert not bucket
