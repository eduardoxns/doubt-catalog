import json


class HttpResponse:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def to_dict(self):
        return {
            'statusCode': self.status_code,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(self.body)
        }


class HttpErrorResponse(HttpResponse):
    def __init__(self, status_code, error_type, message='Unknown Error'):
        super().__init__(status_code, {'error': f'{error_type}: {message}'})


class HttpResponses:
    HTTP_STATUS_OK = 200
    HTTP_STATUS_BAD_REQUEST = 400
    HTTP_STATUS_NOT_FOUND = 404
    HTTP_STATUS_INTERNAL_SERVER_ERROR = 500

    HEADERS_JSON = {'Content-Type': 'application/json'}

    @staticmethod
    def http_response_200(response) -> dict:
        return HttpResponse(
            HttpResponses.HTTP_STATUS_OK,
            json.loads(response)
        ).to_dict()

    @staticmethod
    def http_response_400(response) -> dict:
        return HttpErrorResponse(
            HttpResponses.HTTP_STATUS_BAD_REQUEST,
            'Bad Request', response
        ).to_dict()

    @staticmethod
    def http_response_404(response) -> dict:
        return HttpErrorResponse(
            HttpResponses.HTTP_STATUS_NOT_FOUND,
            'Not Found', response
        ).to_dict()

    @staticmethod
    def http_client_error_response(ce) -> dict:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        return HttpErrorResponse(
            HttpResponses.HTTP_STATUS_INTERNAL_SERVER_ERROR,
            'Internal Server Error', error_message
        ).to_dict()

    @staticmethod
    def http_response_500() -> dict:
        return HttpErrorResponse(
            HttpResponses.HTTP_STATUS_INTERNAL_SERVER_ERROR,
            'Internal Server Error'
        ).to_dict()
