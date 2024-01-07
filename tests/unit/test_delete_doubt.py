import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from src.doubts.delete_doubt import lambda_handler


class BaseTestDeleteDoubt(unittest.TestCase):

    def setUp(self):
        self.mock_table = patch("src.doubts.delete_doubt.dynamodb.Table").start()
        self.mock_delete_item = self.mock_table.return_value.delete_item

    def tearDown(self):
        patch.stopall()

    def generate_event(self, path_parameters=None):
        event = {"pathParameters": path_parameters} if path_parameters else {}
        return event


class TestDeleteDoubt(BaseTestDeleteDoubt):

    def test_delete_doubt_success(self):
        event = self.generate_event(path_parameters={"doubt_id": "mocked_id"})
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"message": "Doubt mocked_id deleted successfully!"}'
        }
        self.assertEqual(response, expected_response)

    def test_delete_doubt_missing_id(self):
        event = self.generate_event(path_parameters={})
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Bad Request: Missing doubt_id in path parameters!"}'
        }
        self.assertEqual(response, expected_response)

    def test_delete_doubt_client_error(self):
        mock_delete_item = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.delete_item.side_effect = mock_delete_item
        event = self.generate_event(path_parameters={"doubt_id": "mocked_id"})
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
