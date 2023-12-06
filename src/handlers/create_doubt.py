import os
import uuid
import json
import boto3
import logging

from datetime import datetime
from src.services.dynamodb import create_table

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Request body is missing or empty'})
        }

    dynamodb_resource = boto3.resource("dynamodb", region_name="sa-east-1")

    try: 
        table_info = dynamodb_resource.Table("doubt_catalog")
    except dynamodb_resource.meta.client.exceptions.ResourceNotFoundException:
        create_table()

    dynamodb_table = dynamodb_resource.Table("doubt_catalog")
    data = json.loads(event.get("body"))

    item = {
        'id': str(uuid.uuid1()),
        'title': data.get("title"),
        'description': data.get("description"),
        'answers': 0,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    dynamodb_table.put_item(Item=item)

    return True