import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb", region_name="sa-east-1")
table = dynamodb.Table("doubt_catalog")


def create_table():
    table_create = dynamodb.create_table(
        TableName="doubt_catalog",
        KeySchema=[
            {
                "AttributeName": "id",
                "KeyType": "HASH"
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    table_create.meta.client.get_waiter('table_exists').wait(TableName=table_create)
    logger.info(f'Table {table_create} created successfully')


if __name__ == "__main__":
    create_table()
