import json
import uuid
import logging
from datetime import datetime
from botocore.exceptions import ClientError
from infra.dynamodb.dynamodb import dynamodb
from src.libraries.utils import verify_if_body_exist, response_200, response_500, client_error_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def create_doubt_item(data):
    return {
        'id': str(uuid.uuid1()),
        'title': data.get("title"),
        'description': data.get("description"),
        'answers': 0,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }


def create_doubt(event):
    verify_if_body_exist(event)

    data = json.loads(event.get("body"))
    item = create_doubt_item(data)

    try:
        dynamodb.Table(TABLE_NAME).put_item(Item=item)
        body = json.dumps(item)
        return response_200(body)

    except ClientError as ce:
        if "Error" in ce.response:
            error_message = ce.response["Error"].get("Message", "Unknown Error")
            logger.exception(f'Error creating doubt: {error_message}')
        else:
            logger.exception(f'Error creating doubt: Unknown Error')
        return client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error creating doubt: {e}')
        return response_500()


def lambda_handler(event, context):
    return create_doubt(event)
