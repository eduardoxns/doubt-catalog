import boto3

dynamodb = boto3.resource("dynamodb", region_name="sa-east-1")


def create_table():
    table = dynamodb.create_table(
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

    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    logger.info(f'Table {table_name} created successfully')
    