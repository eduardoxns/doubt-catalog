import json
import logging
from botocore.exceptions import ClientError

from infra.dynamodb.dynamodb import dynamodb
from src.libraries.exceptions import HttpResponses

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def read_doubts(event):
    try:
        response = dynamodb.Table(TABLE_NAME).scan()
        logger.info(f'Incoming request is: {event}')
        logger.info(f'result: {response}')
        logger.info(f"result[Items]: {response['Items']}")

        items = response.get("Items", [])

        body = json.dumps(items)
        return HttpResponses.http_response_200(body)

    except ClientError as ce:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        logger.exception(f'Error reading doubts: {error_message}')
        return HttpResponses.http_client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error reading doubts: {e}')
        return HttpResponses.http_response_500()


def read_doubt(event):
    params = event.get("pathParameters")
    doubt_id = params.get("doubt_id") if params else None

    if doubt_id is None:
        return HttpResponses.http_response_400("Missing doubt_id in path parameters!")

    try:
        response = dynamodb.Table(TABLE_NAME).get_item(Key={'id': doubt_id})
        item = response.get("Item")

        if not item:
            return HttpResponses.http_response_404("Doubt does not exist!")

        body = json.dumps(item)
        return HttpResponses.http_response_200(body)

    except ClientError as ce:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        logger.exception(f'Error creating doubt: {error_message}')
        return HttpResponses.http_client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error reading doubt: {e}')
        return HttpResponses.http_response_500()


def lambda_handler(event, context):
    route = event.get("path")

    if route == '/doubts':
        return read_doubts(event)
    return read_doubt(event)
