import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from src.doubts.update_doubt import lambda_handler


class BaseTestUpdateDoubt(unittest.TestCase):

    def setUp(self):
        self.mock_table = patch("src.doubts.update_doubt.dynamodb.Table").start()
        self.mock_update_item = self.mock_table.return_value.update_item

    def tearDown(self):
        patch.stopall()

    def generate_event(self, path_parameters=None, body=None):
        event = {
            "pathParameters": path_parameters if path_parameters else None,
            "body": body if body else None
        }
        return event


class TestUpdateDoubt(BaseTestUpdateDoubt):

    def test_update_doubt_success(self):
        mock_update_item = MagicMock()
        self.mock_table.return_value.update_item = mock_update_item
        self.mock_table.return_value.update_item.return_value = {
            'Attributes': {
                'id': 'mocked_id',
                'title': 'Updated Doubt'
            }
        }
        event = self.generate_event(path_parameters={"doubt_id": "mocked_id"}, body='{"title": "Updated Doubt"}')
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"id": "mocked_id", "title": "Updated Doubt"}'
        }
        self.assertEqual(response, expected_response)

    def test_update_doubt_not_found(self):
        self.mock_table.return_value.update_item.return_value = {'Attributes': None}
        event = self.generate_event(path_parameters={"doubt_id": "non_existent_id"}, body='{"title": "Updated Doubt"}')
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Not Found: Doubt does not exist!"}'
        }
        self.assertEqual(response, expected_response)

    def test_update_doubt_missing_id(self):
        event = self.generate_event(path_parameters={})
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Bad Request: Missing doubt_id in path parameters!"}'
        }
        self.assertEqual(response, expected_response)

    def test_update_doubt_client_error(self):
        mock_update_item = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.update_item.side_effect = mock_update_item
        event = self.generate_event(path_parameters={"doubt_id": "mocked_id"}, body='{"title": "Updated Doubt"}')
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
