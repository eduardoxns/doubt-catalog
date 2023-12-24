import json
import logging
from decimal import Decimal
from src.services.dynamodb import table

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def read_doubt(event):
    params = event.get("pathParameters")
    doubt_id = params.get("id") if params else None

    try:
        result = table.get_item(Key={'id': doubt_id})
        item = result.get("Item")
        status_code = 200

        if not item:
            status_code = 404
            item = {'error': f'Doubt {doubt_id} not found!'}

        return {
            'statusCode': status_code,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(item, default=decimal_default)
        }
    except Exception as e:
        logger.error(f'Error reading doubt: {e}', exc_info=True)
        status_code = 500
        return {
            'statusCode': status_code,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal Server Error: {str(e)}'})
        }


def read_doubts(event):
    try:
        result = table.scan()
        logger.info(f'Incoming request is: {event}')
        logger.info(f'result: {result}')
        logger.info(f"result[Items]: {result['Items']}")

        items = result.get("Items", [])

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(items, default=decimal_default)
        }
    except Exception as e:
        logger.error(f'Error reading doubts: {e}', exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal Server Error: {str(e)}'})
        }


def lambda_handler(event, context):
    route = event.get("path")

    if route == '/doubts':
        return read_doubts(event)
    return read_doubt(event)
