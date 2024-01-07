import unittest
from unittest.mock import patch
from src.doubts.delete_doubt import lambda_handler


class TestIntegrationDeleteDoubt(unittest.TestCase):

    @patch("src.doubts.delete_doubt.dynamodb")
    def test_delete_doubt(self, mock_delete_item):
        mock_delete_item.return_value = {}
        event = {"pathParameters": {"doubt_id": "mocked_doubt_id"}}
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"message": "Doubt mocked_doubt_id deleted successfully!"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
