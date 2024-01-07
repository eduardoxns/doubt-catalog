import uuid
import json
import unittest
from unittest.mock import patch
from src.answers.create_answer import lambda_handler


class TestIntegrationCreateAnswer(unittest.TestCase):

    @patch("src.answers.create_answer.dynamodb")
    def test_create_answer(self, mock_create_item):
        mock_create_item.return_value = {}
        event = {
            "body": '{"answer": "Integration Test Answer"}',
            "pathParameters": {"doubt_id": "mocked_doubt_id", "answer_id": "mocked_answer_id"}
        }
        response = lambda_handler(event, context=None)
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response.get('body', '{}'))
        generated_id = response_body.get('id', '')
        self.assertTrue(uuid.UUID(generated_id, version=4))
        response_body.pop('id', None)
        expected_body = {
            "answer": "Integration Test Answer",
            "created_at": response_body.get('created_at'),
        }
        self.assertDictEqual(response_body, expected_body)


if __name__ == '__main__':
    unittest.main()
