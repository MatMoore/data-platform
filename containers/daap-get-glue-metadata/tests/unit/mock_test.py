import json
from moto import mock_glue
import boto3
import pytest
import get_glue_metadata
import json

TEST_DATABASE_NAME = 'test_db'


def glue_table_input(name, location):
    """
    Fake a table input for a Glue catalogue
    """
    return {
        'Name': name,
        'Owner': 'a_fake_owner',
        'Parameters': {
            'EXTERNAL': 'TRUE',
        },
        'Retention': 0,
        'StorageDescriptor': {
            'Location': location,
            'BucketColumns': [],
            'Compressed': False,
            'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
            'NumberOfBuckets': -1,
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
            'Parameters': {},
            'SerdeInfo': {
                'Parameters': {
                    'serialization.format': '1'
                },
                'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
            },
            'SkewedInfo': {
                'SkewedColumnNames': [],
                'SkewedColumnValueLocationMaps': {},
                'SkewedColumnValues': []
            },
            'SortColumns': [],
            'StoredAsSubDirectories': False
        },
        'TableType': 'EXTERNAL_TABLE',
    }


@pytest.fixture
def glue_client():
    """
    Create a mock glue catalogue containing one table.
    """
    with mock_glue():
        client = boto3.client('glue', region_name='us-east-1')
        
        client.create_database(
            DatabaseInput={
                'Name': TEST_DATABASE_NAME
            }
        )

        yield client


def test_success_case(glue_client, monkeypatch):
    test_table_name = 'test_table'
    s3_location = f's3://my-bucket/{TEST_DATABASE_NAME}/{test_table_name}'
    table_input = glue_table_input(test_table_name, s3_location)
    glue_client.create_table(
        DatabaseName=TEST_DATABASE_NAME,
        TableInput=table_input
    )

    # Use the mock client in the lambda, not a real one
    monkeypatch.setattr(boto3, 'client', lambda _name: glue_client)

    event = {
        "queryStringParameters": {
            "database": TEST_DATABASE_NAME,
            "table": test_table_name
        },
    }
    test_response = get_glue_metadata.handler(event, context={})
    body = json.loads(test_response['body'])

    assert test_response['statusCode'] == 200
    assert body['Table'].items() >= table_input.items()
    assert body['ResponseMetadata'].keys() == {'HTTPStatusCode', 'HTTPHeaders', 'RetryAttempts'}
    