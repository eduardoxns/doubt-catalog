import os
import boto3
import logging

dynamodb = boto3.resource("dynamodb")
client = boto3.client("dynamodb")

boto3.resource(
    "dynamodb",
    region_name="sa-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def verify_if_table_exists(table_name: str, dynamodb) -> bool:
    try:
        table = dynamodb.Table(table_name)
        return table.table_status == 'ACTIVE'
    except dynamodb.meta.client.exceptions.ResourceNotFoundException as err:
        logging.info(err)
        return False


def create_table(table_name, table_info):
    if not verify_if_table_exists(table_name, dynamodb):
        response = dynamodb.create_table(**table_info())
        response.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        logging.info("Table successfully created! {}".format(response))

    return table_name
