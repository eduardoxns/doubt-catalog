import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError

from src.answers.read_answer import lambda_handler


class BaseTestReadAnswer(unittest.TestCase):

    def setUp(self):
        self.mock_table = patch("src.answers.read_answer.dynamodb.Table").start()
        self.mock_read_item = self.mock_table.return_value.put_item

    def tearDown(self):
        patch.stopall()

    def generate_event(self, path_parameters=None, path=None):
        event = {
            "pathParameters": path_parameters if path_parameters else None,
            "path": path if path else None
        }
        return event


class TestReadAnswers(BaseTestReadAnswer):

    def test_read_answers_success(self):
        self.mock_table.return_value.get_item.return_value = {
            "Item": {
                "id": "mocked__doubt_id",
                "answers": [{"id": "1", "answer": "Answer 1"}, {"id": "2", "answer": "Answer 2"}]
            }
        }
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers",
                                    path_parameters={"doubt_id": "mocked_doubt_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '[{"id": "1", "answer": "Answer 1"}, {"id": "2", "answer": "Answer 2"}]'
        }
        self.assertEqual(response, expected_response)

    def test_read_answers_missing_doubt_id(self):
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers", path_parameters={"doubt_id": ""})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Bad Request: Missing doubt_id in path parameters!"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_answers_doubt_not_found(self):
        self.mock_table.return_value.get_item.return_value = {"Item": None}
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers",
                                    path_parameters={"doubt_id": "mocked_doubt_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Not Found: Doubt does not exist!"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_answers_client_error(self):
        mock_read_item = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.get_item.side_effect = mock_read_item
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers",
                                    path_parameters={"doubt_id": "mocked_doubt_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)


class TestReadAnswer(BaseTestReadAnswer):
    def test_read_answer_success(self):
        self.mock_table.return_value.get_item.return_value = {
            "Item": {
                "id": "mocked_doubt_id",
                "answers": [{"id": "mocked_answer_id", "answer": "Test Answer"}]
            }
        }
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers/mocked_answer_id",
                                    path_parameters={"doubt_id": "mocked_doubt_id", "answer_id": "mocked_answer_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"id": "mocked_answer_id", "answer": "Test Answer"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_answer_missing_doubt_id(self):
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers/mocked_answer_id",
                                    path_parameters={"doubt_id": "", "answer_id": "mocked_answer_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Bad Request: Missing doubt_id in path parameters!"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_answer_missing_answer_id(self):
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers/mocked_answer_id",
                                    path_parameters={"doubt_id": "mocked_doubt_id", "answer_id": ""})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Bad Request: Missing answer_id in path parameters!"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_answer_doubt_not_found(self):
        self.mock_table.return_value.get_item.return_value = {"Item": None}
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers/mocked_answer_id",
                                    path_parameters={"doubt_id": "mocked_doubt_id", "answer_id": "mocked_answer_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Not Found: Doubt does not exist!"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_answer_answer_not_found(self):
        self.mock_table.return_value.get_item.return_value = {"Item": {"id": "mocked_doubt_id", "answers": []}}
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers/answer_id",
                                    path_parameters={"doubt_id": "mocked_doubt_id", "answer_id": "answer_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Not Found: Answer does not exist!"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_answer_client_error(self):
        mock_read_item = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.get_item.side_effect = mock_read_item
        event = self.generate_event(path="/doubts/mocked_doubt_id/answers/mocked_answer_id",
                                    path_parameters={"doubt_id": "mocked_doubt_id", "answer_id": "mocked_answer_id"})
        response = lambda_handler(event, context=None)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
