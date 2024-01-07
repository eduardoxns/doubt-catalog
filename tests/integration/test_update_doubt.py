import json
import unittest
from unittest.mock import patch
from src.doubts.update_doubt import lambda_handler


class TestIntegrationUpdateDoubt(unittest.TestCase):

    @patch("src.doubts.update_doubt.dynamodb.Table")
    def test_update_doubt(self, mock_update_item):
        mock_update_item.return_value.update_item.return_value = {
            'Attributes': {
                'id': 'mocked_doubt_id',
                'title': 'Updated Doubt'
            }
        }
        event = {
            "pathParameters": {"doubt_id": "mocked_doubt_id"},
            "body": json.dumps({"title": "Updated Doubt"})
        }
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"id": "mocked_doubt_id", "title": "Updated Doubt"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
