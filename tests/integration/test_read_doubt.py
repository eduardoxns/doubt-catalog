import unittest
from unittest.mock import patch
from src.doubts.read_doubt import lambda_handler


class TestIntegrationReadDoubt(unittest.TestCase):

    @patch("src.doubts.read_doubt.dynamodb.Table")
    def test_read_doubts(self, mock_read_item):
        mock_read_item.return_value.scan.return_value = {
            "Items": [
                {
                    "id": "1",
                    "title": "Doubt 1"
                },
                {
                    "id": "2",
                    "title": "Doubt 2"
                }
            ]
        }
        event = {"path": "/doubts"}
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '[{"id": "1", "title": "Doubt 1"}, {"id": "2", "title": "Doubt 2"}]'
        }
        self.assertEqual(response, expected_response)

    @patch("src.doubts.read_doubt.dynamodb.Table")
    def test_read_doubt(self, mock_read_item):
        mock_read_item.return_value.get_item.return_value = {
            "Item": {
                "id": "mocked_id",
                "title": "Test Doubt"
            }
        }
        event = {"pathParameters": {"doubt_id": "mocked_id"}}
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"id": "mocked_id", "title": "Test Doubt"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
