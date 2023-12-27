import json
import logging
from botocore.exceptions import ClientError
from infra.dynamodb.dynamodb import dynamodb
from src.libraries.exceptions import HttpResponses

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def lambda_handler(event, context):
    doubt_id = event.get("pathParameters", {}).get("id")

    if not doubt_id:
        return HttpResponses.http_response_400("Missing doubt_id in path parameters!")

    try:
        dynamodb.Table(TABLE_NAME).delete_item(Key={'id': doubt_id})
        body = json.dumps({'message': f'Doubt {doubt_id} deleted successfully!'})
        return HttpResponses.http_response_200(body)

    except ClientError as ce:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        logger.exception(f'Error deleting doubt: {error_message}')
        return HttpResponses.http_client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error deleting doubt: {e}')
        return HttpResponses.http_response_500()
