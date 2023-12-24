import json
import logging
from datetime import datetime
from decimal import Decimal

from src.services.dynamodb import table

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def lambda_handler(event, context):
    params = event.get("pathParameters")
    doubt_id = params.get("id") if params else None

    if 'body' not in event:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Request body is missing or empty'})
        }

    data = json.loads(event.get("body"))

    try:
        response = table.update_item(
            Key={'id': doubt_id},
            UpdateExpression='SET title = :title, description = :description, updated_at = :updated_at',
            ExpressionAttributeValues={
                ':title': data.get("title"),
                ':description': data.get("description"),
                ':updated_at': datetime.now().isoformat()
            },
            ReturnValues='ALL_NEW'
        )
        updated_item = response.get("Attributes")

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(updated_item, default=decimal_default)
        }
    except Exception as e:
        logger.error(f'Error updating doubt: {e}', exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal Server Error: {str(e)}'})
        }
