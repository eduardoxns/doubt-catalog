import json
import logging
from botocore.exceptions import ClientError
from infra.dynamodb.dynamodb import dynamodb
from src.libraries.utils import response_200, response_400, response_500, client_error_response

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def lambda_handler(event, context):
    params = event.get("pathParameters")
    doubt_id = params.get("id") if params else None

    if doubt_id is None:
        return response_400()

    try:
        dynamodb.Table(TABLE_NAME).delete_item(Key={'id': doubt_id})
        body = json.dumps({'message': f'Doubt {doubt_id} deleted successfully'})
        return response_200(body)

    except ClientError as ce:
        if "Error" in ce.response:
            error_message = ce.response["Error"].get("Message", "Unknown Error")
            logger.exception(f'Error deleting doubt: {error_message}')
        else:
            logger.exception(f'Error deleting doubt: Unknown Error')
        return client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error deleting doubt: {e}')
        return response_500()
