import json
import logging
from botocore.exceptions import ClientError
from src.infra.dynamodb.dynamodb import dynamodb
from src.utils.utils import response_200, response_400, response_500, client_error_response

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
        logger.exception(f'Error deleting doubt: {ce.response["Error"]["Message"]}')
        return client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error deleting doubt: {e}')
        return response_500()
