import json
import uuid
import logging
from datetime import datetime
from botocore.exceptions import ClientError

from infra.dynamodb.dynamodb import dynamodb
from src.libraries.exceptions import HttpResponses
from src.libraries.utils import verify_if_body_exist, MissingBodyError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def create_answer_item(data):
    return {
        'id': str(uuid.uuid1()),
        'answer': data.get("answer"),
        'created_at': datetime.now().isoformat()
    }


def lambda_handler(event, context):
    params = event.get("pathParameters")
    doubt_id = params.get("doubt_id") if params else None

    if not doubt_id:
        return HttpResponses.http_response_400("Missing doubt_id in path parameters!")

    try:
        data = json.loads(event.get("body"))
        verify_if_body_exist(event)
        doubt = dynamodb.Table(TABLE_NAME).get_item(Key={'id': doubt_id}).get('Item')

        if not doubt:
            return HttpResponses.http_response_404(f"Doubt with ID {doubt_id} not found!")

        answer_item = create_answer_item(data)
        doubt['answers'].append(answer_item)

        dynamodb.Table(TABLE_NAME).put_item(Item=doubt)
        body = json.dumps(answer_item)
        return HttpResponses.http_response_200(body)

    except MissingBodyError:
        return HttpResponses.http_response_404("Request body not found!")

    except ClientError as ce:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        logger.exception(f'Error creating answer: {error_message}')
        return HttpResponses.http_client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error creating answer: {e}')
        return HttpResponses.http_response_500()
