import json
import logging
from datetime import datetime
from botocore.exceptions import ClientError
from infra.dynamodb.dynamodb import dynamodb
from src.libraries.utils import decimal_default, verify_if_body_exist, response_200, response_404, response_500, client_error_response

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

    verify_if_body_exist(event)
    data = json.loads(event.get("body"))

    try:
        response = dynamodb.Table(TABLE_NAME).update_item(**update_doubt_item(doubt_id, data))
        updated_item = response.get("Attributes")
        body = json.dumps(updated_item, default=decimal_default)
        return response_200(body)

    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        return response_404()

    except ClientError as ce:
        logger.exception(f'Error updating doubt: {ce.response["Error"]["Message"]}')
        return client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error updating doubt: {e}')
        return response_500()
