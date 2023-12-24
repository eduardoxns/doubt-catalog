import json
import logging
from src.services.dynamodb import table

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    params = event.get("pathParameters")
    doubt_id = params.get("id") if params else None

    try:
        response = table.delete_item(
            Key={'id': doubt_id}
        )
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': f'Doubt {doubt_id} deleted successfully'})
        }
    except Exception as e:
        logger.error(f'Error deleting doubt: {e}', exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal Server Error: {str(e)}'})
        }
