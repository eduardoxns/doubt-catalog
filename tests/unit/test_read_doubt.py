import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError

from src.doubts.read_doubt import lambda_handler


class BaseTestReadDoubt(unittest.TestCase):

    def setUp(self):
        self.mock_table = patch("src.doubts.read_doubt.dynamodb.Table").start()
        self.mock_read_item = self.mock_table.return_value.read_item

    def tearDown(self):
        patch.stopall()

    def generate_event(self, path_parameters=None, path=None):
        event = {
            "pathParameters": path_parameters if path_parameters else None,
            "path": path if path else None
        }
        return event


class TestReadDoubts(BaseTestReadDoubt):

    def test_read_doubts_success(self):
        self.mock_table.return_value.scan.return_value = {
            "Items": [
                {"id": "1", "title": "Doubt 1"},
                {"id": "2", "title": "Doubt 2"}
            ]
        }
        event = self.generate_event(path="/doubts")
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '[{"id": "1", "title": "Doubt 1"}, {"id": "2", "title": "Doubt 2"}]'
        }
        self.assertEqual(response, expected_response)

    def test_read_doubts_client_error(self):
        mock_read_item = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.scan.side_effect = mock_read_item
        event = self.generate_event(path="/doubts")
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)


class TestReadDoubt(BaseTestReadDoubt):

    def test_read_doubt_success(self):
        self.mock_table.return_value.get_item.return_value = {
            "Item": {
                "id": "mocked_doubt_id",
                "title": "Test Doubt"
            }
        }
        event = self.generate_event(path_parameters={"doubt_id": "mocked_doubt_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"id": "mocked_doubt_id", "title": "Test Doubt"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_doubt_not_found(self):
        self.mock_table.return_value.get_item.return_value = {"Item": None}
        event = self.generate_event(path_parameters={"doubt_id": "non_existent_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Not Found: Doubt does not exist!"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_doubt_client_error(self):
        mock_read_item = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.get_item.side_effect = mock_read_item
        event = self.generate_event(path_parameters={"doubt_id": "mocked_doubt_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
