import json
import logging
from botocore.exceptions import ClientError

from infra.dynamodb.dynamodb import dynamodb
from src.libraries.exceptions import HttpResponses
from src.libraries.utils import decimal_default

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def read_answer(event):
    params = event.get("pathParameters")
    doubt_id = params.get("doubt_id") if params else None
    answer_id = params.get("answer_id") if params else None

    if not doubt_id or not answer_id:
        return HttpResponses.http_response_400("Missing doubt_id or answer_id in path parameters!")

    try:
        response = dynamodb.Table(TABLE_NAME).get_item(Key={'id': doubt_id})
        item = response.get("Item")

        if not item:
            return HttpResponses.http_response_404("Doubt does not exist!")

        answers = item.get("answers", [])
        specific_answer = next((answer for answer in answers if answer.get("id") == answer_id), None)

        if not specific_answer:
            return HttpResponses.http_response_404("Answer does not exist!")

        body = json.dumps(specific_answer, default=decimal_default)
        return HttpResponses.http_response_200(body)

    except ClientError as ce:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        logger.exception(f'Error reading doubt: {error_message}')
        return HttpResponses.http_client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error reading doubt: {e}')
        return HttpResponses.http_response_500()


def read_answers(event):
    params = event.get("pathParameters")
    doubt_id = params.get("doubt_id") if params else None

    if not doubt_id:
        return HttpResponses.http_response_400("Missing doubt_id in path parameters!")

    try:
        response = dynamodb.Table(TABLE_NAME).get_item(Key={'id': doubt_id})
        item = response.get("Item")

        if not item:
            return HttpResponses.http_response_404("Doubt does not exist!")

        answers = item.get("answers", [])

        body = json.dumps(answers, default=decimal_default)
        return HttpResponses.http_response_200(body)

    except ClientError as ce:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        logger.exception(f'Error reading doubt: {error_message}')
        return HttpResponses.http_client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error reading doubt: {e}')
        return HttpResponses.http_response_500()


def lambda_handler(event, context):
    route = event.get("path")
    doubt_id = event.get("pathParameters", {}).get("doubt_id")

    if route == f'/doubts/{doubt_id}/answers':
        return read_answers(event)
    return read_answer(event)
