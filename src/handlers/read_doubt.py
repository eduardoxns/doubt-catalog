import json
import logging
from botocore.exceptions import ClientError
from src.infra.dynamodb.dynamodb import dynamodb
from src.utils.utils import decimal_default, response_200, response_400, response_404, response_500, client_error_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def read_doubt(event):
    params = event.get("pathParameters")
    doubt_id = params.get("id") if params else None

    if doubt_id is None:
        return response_400()

    try:
        response = dynamodb.Table(TABLE_NAME).get_item(Key={'id': doubt_id})
        item = response.get("Item")

        if not item:
            return response_404()

        body = json.dumps(item, default=decimal_default)
        return response_200(body)

    except ClientError as ce:
        logger.exception(f'Error reading doubt: {ce.response["Error"]["Message"]}')
        return client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error reading doubt: {e}')
        return response_500()


def read_doubts(event):
    try:
        response = dynamodb.Table(TABLE_NAME).scan()
        logger.info(f'Incoming request is: {event}')
        logger.info(f'result: {response}')
        logger.info(f"result[Items]: {response['Items']}")

        items = response.get("Items", [])

        body = json.dumps(items, default=decimal_default)
        return response_200(body)

    except ClientError as ce:
        logger.exception(f'Error reading doubts: {ce.response["Error"]["Message"]}')
        return client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error reading doubts: {e}')
        return response_500()


def lambda_handler(event, context):
    route = event.get("path")

    if route == '/doubts':
        return read_doubts(event)
    return read_doubt(event)
