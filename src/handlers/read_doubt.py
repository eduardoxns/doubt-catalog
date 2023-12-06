import logging

from src.services.dynamodb import dynamodb

logger = logging.getLogger()
logger.setLevel(logging.INFO)

table = dynamodb.Table("doubt_catalog")


def read_doubt(event):
    params = event.get("pathParameters")
    doubt_id = params.get("id")

    result = table.get_item(
        Key={'id': doubt_id}
    )
    item = result.get("Item")
    status_code = 200

    if not item:
        status_code = 404
        item = f'{doubt_id} not found!'

    return item


def read_doubts(event):
    result = table.scan()
    logger.info(f'Incoming request is: {event}')
    logger.info(f'result: {result}')
    logger.info(f"result[Items]: {result['Items']}")

    item = result.get("Items")

    return item


def lambda_handler(event, context):
    route = event.get("path")

    if route == '/doubts':
        return read_doubts(event)
    return read_doubt(event)
