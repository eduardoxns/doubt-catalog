import os
import boto3
import logging

logging.basicConfig(level=logging.INFO)
dynamodb = boto3.resource("dynamodb", region_name=os.getenv("AWS_DEFAULT_REGION"))


def verify_if_table_exists(table_name: str) -> bool:
    try:
        table = dynamodb.Table(table_name)
        return table.table_status == 'ACTIVE'
    except dynamodb.meta.client.exceptions.ResourceNotFoundException as err:
        logging.info(err)
        return False


def create_table(table_name, table_info_func):
    if not verify_if_table_exists(table_name):
        table_info = table_info_func()
        response = dynamodb.create_table(**table_info)
        response.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        logging.info("Table successfully created! {}".format(response))
    else:
        logging.info("Table already exists.")

    return table_name
