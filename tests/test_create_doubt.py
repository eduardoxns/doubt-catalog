import json
import uuid
import unittest
from unittest.mock import patch, MagicMock

from botocore.exceptions import ClientError

from src.doubts.create_doubt import create_doubt


class BaseTestCreateDoubt(unittest.TestCase):

    def setUp(self):
        self.mock_table = patch("src.doubts.create_doubt.dynamodb.Table").start()

    def tearDown(self):
        patch.stopall()

    def generate_event(self, body=None):
        return {"body": body} if body else {}


class TestCreateDoubt(BaseTestCreateDoubt):

    def test_create_doubt_success(self):
        mock_put_item = MagicMock()
        self.mock_table.return_value.put_item = mock_put_item

        event = self.generate_event(
            body='{"title": "Test Doubt","description": "This is a test doubt"}'
        )
        response = create_doubt(event)

        self.assertEqual(response['statusCode'], 200)

        response_body = json.loads(response.get('body', '{}'))
        self.assertTrue(uuid.UUID(response_body.get('id', ''), version=4))
        response_body.pop('id', None)

        expected_body = {
            "title": "Test Doubt",
            "description": "This is a test doubt",
            "answers": 0,
            "created_at": response_body.get('created_at'),
            "updated_at": response_body.get('updated_at')
        }
        self.assertDictEqual(response_body, expected_body)

    def test_create_doubt_missing_body(self):
        self.mock_table.return_value.put_item.side_effect = ValueError('Request body is missing or empty')
        event = self.generate_event(body='{}')
        response = create_doubt(event)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error"}'
        }
        self.assertEqual(response, expected_response)

    def test_create_doubt_client_error(self):
        mock_put_item = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.put_item = mock_put_item
        event = self.generate_event(
            body='{"title": "Test Doubt","description": "This is a test doubt"}'
        )
        response = create_doubt(event)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)

    def test_create_doubt_generic_error(self):
        mock_put_item = MagicMock(side_effect=Exception("Unexpected error"))
        self.mock_table.return_value.put_item = mock_put_item
        event = self.generate_event(
            body='{"title": "Test Doubt","description": "This is a test doubt"}'
        )
        response = create_doubt(event)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
