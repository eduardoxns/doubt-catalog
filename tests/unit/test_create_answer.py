import json
import uuid
import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError

from src.answers.create_answer import lambda_handler
from src.libraries.utils import MissingBodyError


class BaseTestCreateAnswer(unittest.TestCase):

    def setUp(self):
        self.mock_table = patch("src.answers.create_answer.dynamodb.Table").start()
        self.mock_create_item = self.mock_table.return_value.put_item

    def tearDown(self):
        patch.stopall()

    def generate_event(self, path_parameters=None, body=None):
        event = {
            "pathParameters": path_parameters if path_parameters else None,
            "body": body if body else None
        }
        return event


class TestCreateAnswer(BaseTestCreateAnswer):

    def test_create_answer_success(self):
        mock_create_item = MagicMock()
        self.mock_table.return_value.put_item = mock_create_item
        event = self.generate_event(path_parameters={"doubt_id": "mocked_id"}, body='{"answer": "Test Answer"}')
        response = lambda_handler(event, context=None)
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response.get('body', '{}'))
        generated_id = response_body.get('id', '')
        self.assertTrue(uuid.UUID(generated_id, version=4))
        response_body.pop('id', None)
        expected_body = {
            "answer": "Test Answer",
            "created_at": response_body.get('created_at')
        }
        self.assertDictEqual(response_body, expected_body)

    def test_create_answer_missing_body(self):
        mock_create_item = MagicMock(side_effect=MissingBodyError("Request body is missing or empty"))
        self.mock_table.return_value.put_item = mock_create_item
        event = self.generate_event(path_parameters={"doubt_id": "mocked_id"}, body='{}')
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Not Found: Request body not found!"}'
        }
        self.assertEqual(response, expected_response)

    def test_create_answer_missing_doubt_id(self):
        event = self.generate_event(path_parameters={"doubt_id": ""}, body='{"answer": "Test Answer"}')
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Bad Request: Missing doubt_id in path parameters!"}'
        }
        self.assertEqual(response, expected_response)

    def test_create_answer_doubt_not_found(self):
        self.mock_table.return_value.get_item.return_value = {"Item": None}
        event = self.generate_event(path_parameters={"doubt_id": "non_existent_id"}, body='{}')
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Not Found: Doubt with ID non_existent_id not found!"}'
        }
        self.assertEqual(response, expected_response)

    def test_create_answer_client_error(self):
        mock_create_item = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.put_item = mock_create_item
        event = self.generate_event(path_parameters={"doubt_id": "mocked_id"}, body='{"answer": "Test Answer"}')
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
