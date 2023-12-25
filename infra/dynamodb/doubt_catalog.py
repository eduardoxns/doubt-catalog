import logging
from dynamodb import create_table

logging.getLogger().setLevel(logging.INFO)

__table_name__ = "doubt_catalog"


def table_info():
    info = {
        "TableName": __table_name__,
        "KeySchema": [
            {
                "AttributeName": "id",
                "KeyType": "HASH",
            }
        ],
        "AttributeDefinitions": [
            {
                "AttributeName": "id",
                "AttributeType": "S"
            }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        }
    }
    return info


if __name__ == "__main__":
    table_name = create_table(__table_name__, table_info)
    logging.info("Done!")
