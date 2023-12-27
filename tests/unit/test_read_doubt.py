import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from src.doubts.read_doubt import read_doubt, read_doubts


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


class TestReadDoubt(BaseTestReadDoubt):

    def test_read_doubt_success(self):
        self.mock_table.return_value.get_item.return_value = {"Item": {"id": "mocked_id", "title": "Test Doubt"}}
        event = self.generate_event(path_parameters={"id": "mocked_id"})
        response = read_doubt(event)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"id": "mocked_id", "title": "Test Doubt"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_doubt_not_found(self):
        self.mock_table.return_value.get_item.return_value = {"Item": None}
        event = self.generate_event(path_parameters={"id": "non_existent_id"})
        response = read_doubt(event)
        expected_response = {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Not Found: Doubt does not exist!"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_doubt_client_error(self):
        doubt_id = "mocked_id"
        mock_client_error = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.get_item.side_effect = mock_client_error
        event = self.generate_event(path_parameters={"id": doubt_id})
        response = read_doubt(event)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_doubt_generic_error(self):
        mock_client_error = MagicMock()
        mock_client_error.response.__getitem__.return_value = {"Error": {"Message": "Mocked error"}}
        self.mock_table.return_value.get_item.side_effect = mock_client_error
        event = self.generate_event(path_parameters={"id": "some_id"})
        response = read_doubt(event)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error"}'
        }
        self.assertEqual(response, expected_response)


class TestReadDoubts(BaseTestReadDoubt):

    def test_read_doubts_success(self):
        self.mock_table.return_value.scan.return_value = {
            "Items":
                [
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
        event = self.generate_event(path="/doubts")
        response = read_doubts(event)
        expected_response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': '[{"id": "1", "title": "Doubt 1"}, {"id": "2", "title": "Doubt 2"}]'
        }
        self.assertEqual(response, expected_response)

    def test_read_doubts_client_error(self):
        mock_client_error = MagicMock(side_effect=ClientError({}, "operation_name"))
        self.mock_table.return_value.scan.side_effect = mock_client_error
        event = self.generate_event(path="/doubts")
        response = read_doubts(event)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error: Unknown Error"}'
        }
        self.assertEqual(response, expected_response)

    def test_read_doubts_generic_error(self):
        self.mock_table.return_value.scan.side_effect = Exception("Unexpected error")
        event = self.generate_event(path="/doubts")
        response = read_doubts(event)
        expected_response = {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal Server Error"}'
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
