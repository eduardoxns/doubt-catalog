import json
import logging
from datetime import datetime
from botocore.exceptions import ClientError

from infra.dynamodb.dynamodb import dynamodb
from src.libraries.exceptions import HttpResponses
from src.libraries.utils import decimal_default, verify_if_body_exist, MissingBodyError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def update_item(doubt_id, data):
    return {
        'Key': {'id': doubt_id},
        'UpdateExpression': 'SET title = :title, description = :description, updated_at = :updated_at',
        'ExpressionAttributeValues': {
            ':title': data.get("title"),
            ':description': data.get("description"),
            ':updated_at': datetime.now().isoformat()
        },
        'ReturnValues': 'ALL_NEW'
    }


def lambda_handler(event, context):
    params = event.get("pathParameters")
    doubt_id = params.get("doubt_id") if params else None

    if not doubt_id:
        return HttpResponses.http_response_400("Missing doubt_id in path parameters!")

    try:
        data = json.loads(event.get("body"))
        verify_if_body_exist(event)

        response = dynamodb.Table(TABLE_NAME).update_item(**update_item(doubt_id, data))
        item = response.get("Attributes")

        if not item:
            return HttpResponses.http_response_404("Doubt does not exist!")

        body = json.dumps(item, default=decimal_default)
        return HttpResponses.http_response_200(body)

    except MissingBodyError as mbe:
        return HttpResponses.http_response_404("Request body not found!")

    except ClientError as ce:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        logger.exception(f'Error updating doubt: {error_message}')
        return HttpResponses.http_client_error_response(ce)

    except Exception as e:
        logger.error(f'Unexpected error updating doubt: {e}')
        return HttpResponses.http_response_500()
