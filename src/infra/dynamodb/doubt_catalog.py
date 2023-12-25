import logging
from dynamodb import create_table

logging.getLogger().setLevel(logging.INFO)

_table_name = "doubt_catalog"


def table_info():
    info = {
        "TableName": _table_name,
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
    table_name = create_table(_table_name, table_info)
    logging.info("Done!")
