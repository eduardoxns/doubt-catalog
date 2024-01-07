import uuid
import json
import unittest
from unittest.mock import patch
from src.doubts.create_doubt import lambda_handler


class TestIntegrationCreateDoubt(unittest.TestCase):

    @patch("src.doubts.create_doubt.dynamodb")
    def test_create_doubt(self, mock_create_item):
        mock_create_item.return_value = {}
        body_data = {
            "title": "Integration Test Doubt",
            "description": "This is an integration test doubt"
        }
        event = {"body": json.dumps(body_data)}
        response = lambda_handler(event, context=None)
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response.get('body', '{}'))
        generated_id = response_body.get('id', '')
        self.assertTrue(uuid.UUID(generated_id, version=4))
        response_body.pop('id', None)
        expected_body = {
            "title": "Integration Test Doubt",
            "description": "This is an integration test doubt",
            "answers": [],
            "created_at": response_body.get('created_at'),
            "updated_at": response_body.get('updated_at')
        }
        self.assertDictEqual(response_body, expected_body)


if __name__ == '__main__':
    unittest.main()
