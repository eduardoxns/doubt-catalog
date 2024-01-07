import json
import uuid
import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from moto import mock_dynamodb

from src.doubts.create_doubt import lambda_handler
from src.libraries.utils import MissingBodyError


@mock_dynamodb
class BaseTestCreateDoubt(unittest.TestCase):

    def setUp(self):
        self.mock_table_name = 'doubt_catalog'
        self.mock_create_item = MagicMock()
        self.mock_table = patch("src.doubts.create_doubt.dynamodb.Table").start()
        self.mock_table.return_value.put_item = self.mock_create_item

    def tearDown(self):
        patch.stopall()

    def generate_event(self, body=None):
        return {"body": body} if body else {}


class TestCreateDoubt(BaseTestCreateDoubt):

    def test_create_doubt_success(self):
        mock_create_item = MagicMock()
        self.mock_table.return_value.put_item = mock_create_item
        event = self.generate_event(body='{"title": "Test Doubt","description": "This is a test doubt"}')
        response = lambda_handler(event, context=None)
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response.get('body', '{}'))
        generated_id = response_body.get('id', '')
        self.assertTrue(uuid.UUID(generated_id, version=4))
        response_body.pop('id', None)
        expected_body = {
            "title": "Test Doubt",
            "description": "This is a test doubt",
            "answers": [],
            "created_at": response_body.get('created_at'),
            "updated_at": response_body.get('updated_at')
        }
        self.assertDictEqual(response_body, expected_body)

    def test_create_doubt_missing_body(self):
        mock_create_item = MagicMock(side_effect=MissingBodyError("Request body is missing or empty"))
        self.mock_table.return_value.put_item = mock_create_item
        event = self.generate_event(body='{}')
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Not Found: Request body not found!"}'
        }
        self.assertEqual(response, expected_response)

    def test_create_doubt_client_error(self):
        mock_create_item = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.put_item = mock_create_item
        event = self.generate_event(body='{"title": "Test Doubt","description": "This is a test doubt"}')
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
