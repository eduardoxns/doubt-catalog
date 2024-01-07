import unittest
from unittest.mock import patch
from src.answers.read_answer import lambda_handler


class TestIntegrationReadAnswer(unittest.TestCase):

    @patch("src.answers.read_answer.dynamodb.Table")
    def test_read_answers(self, mock_read_item):
        mock_read_item.return_value.get_item.return_value = {
            "Item": {
                "id": "mocked_doubt_id",
                "answers": [{"id": "1", "answer": "Answer 1"}, {"id": "2", "answer": "Answer 2"}]
            }
        }
        event = {
            "path": "/doubts/mocked_doubt_id/answers",
            "pathParameters": {"doubt_id": "mocked_doubt_id"}
        }
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '[{"id": "1", "answer": "Answer 1"}, {"id": "2", "answer": "Answer 2"}]'
        }
        self.assertEqual(response, expected_response)

    @patch("src.answers.read_answer.dynamodb.Table")
    def test_read_answer(self, mock_read_item):
        mock_read_item.return_value.get_item.return_value = {
            "Item": {
                "id": "mocked_doubt_id",
                "answers": [{"id": "mocked_answer_id", "answer": "Test Answer"}]
            }
        }
        event = {
            "path": "/doubts/mocked_doubt_id/answers/mocked_answer_id",
            "pathParameters": {"doubt_id": "mocked_doubt_id", "answer_id": "mocked_answer_id"}
        }
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"id": "mocked_answer_id", "answer": "Test Answer"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
