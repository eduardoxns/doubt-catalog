import os
import json
import boto3
import logging

from src.libraries.utils import http_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_resource = boto3.resource("dynamodb", region_name="sa-east-1")
dynamodb_table = dynamodb_resource.Table("doubt_catalog")

def read_doubt(event):
    params = event.get("pathParameters")
    doubt_id = params.get("id")

    result = dynamodb_table.get_item(
        Key = {'id': doubt_id}
    )

    item = result.get("Item")
    status_code = 200

    if not item:
        status_code = 404
        item = f'{doubt_id} not found!'

    return item


def read_doubts(event):
    result = dynamodb_table.scan()
    logger.info(f'Incoming request is: {event}')
    logger.info(f'result: {result}')
    logger.info(f"result[Items]: {result['Items']}")

    item = result.get("Items")

    return item


def lambda_handler(event, context):
    route = event.get("path")

    if route == '/doubts':
        return read_doubts(event)
    return read_doubt(event)