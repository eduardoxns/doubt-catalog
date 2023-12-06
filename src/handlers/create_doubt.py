import uuid
import json
import logging
from datetime import datetime
from src.services.dynamodb import dynamodb

logger = logging.getLogger()
logger.setLevel(logging.INFO)

table = dynamodb.Table("doubt_catalog")


def lambda_handler(event, context):
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Request body is missing or empty'})
        }

    data = json.loads(event.get("body"))

    item = {
        'id': str(uuid.uuid1()),
        'title': data.get("title"),
        'description': data.get("description"),
        'answers': 0,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    table.put_item(Item=item)

    return True
