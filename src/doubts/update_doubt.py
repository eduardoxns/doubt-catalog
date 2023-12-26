import json
import logging
from datetime import datetime
from botocore.exceptions import ClientError
from infra.dynamodb.dynamodb import dynamodb
from src.libraries.utils import decimal_default, verify_if_body_exist, response_200, response_404, response_500, \
    client_error_response, response_400

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def update_doubt_item(doubt_id, data):
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
    doubt_id = params.get("id") if params else None

    if not doubt_id:
        return response_400()

    verify_if_body_exist(event)
    data = json.loads(event.get("body"))

    try:
        response = dynamodb.Table(TABLE_NAME).update_item(**update_doubt_item(doubt_id, data))
        updated_item = response.get("Attributes")

        if not updated_item:
            return response_404()

        body = json.dumps(updated_item, default=decimal_default)
        return response_200(body)

    except ClientError as ce:
        if "Error" in ce.response:
            error_message = ce.response["Error"].get("Message", "Unknown Error")
            logger.error(f'Error updating doubt: {error_message}')
        else:
            logger.error(f'Error updating doubt: Unknown Error')
        return client_error_response(ce)

    except Exception as e:
        logger.error(f'Unexpected error updating doubt: {e}')
        return response_500()
