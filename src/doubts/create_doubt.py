import json
import uuid
import logging
from datetime import datetime
from botocore.exceptions import ClientError

from infra.dynamodb.dynamodb import dynamodb
from src.libraries.exceptions import HttpResponses
from src.libraries.utils import MissingBodyError, verify_if_body_exist, reorder_json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def create_item(data):
    return {
        'id': str(uuid.uuid1()),
        'title': data.get("title"),
        'description': data.get("description"),
        'answers': [],
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }


def lambda_handler(event, context):
    try:
        data = json.loads(event.get("body"))
        verify_if_body_exist(event)

        item = create_item(data)
        dynamodb.Table(TABLE_NAME).put_item(Item=item)

        body = json.dumps(reorder_json(item))
        return HttpResponses.http_response_200(body)

    except MissingBodyError:
        return HttpResponses.http_response_404("Request body not found!")

    except ClientError as ce:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        logger.exception(f'Error creating doubt: {error_message}')
        return HttpResponses.http_client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error creating doubt: {e}')
        return HttpResponses.http_response_500()
