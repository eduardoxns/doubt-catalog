import unittest
from unittest.mock import patch
from src.answers.delete_answer import lambda_handler


class TestIntegrationAnswerDoubt(unittest.TestCase):

    @patch("src.answers.delete_answer.dynamodb.Table")
    def test_delete_answer(self, mock_delete_item):
        mock_delete_item.return_value.get_item.return_value = {
            "Item": {
                "id": "mocked_doubt_id",
                "answers": [{"id": "mocked_answer_id", "answer": "Test Answer"}]
            }
        }
        event = {"pathParameters": {"doubt_id": "mocked_doubt_id", "answer_id": "mocked_answer_id"}}
        response = lambda_handler(event, None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"message": "Answer mocked_answer_id deleted successfully from doubt mocked_doubt_id!"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
