import json
import logging
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

HEADERS_JSON = {'Content-Type': 'application/json'}
HTTP_STATUS_OK = 200
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500


def verify_if_body_exist(event):
    if 'body' not in event:
        raise ValueError('Request body is missing or empty')


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def response_200(body) -> dict:
    return {
        'statusCode': HTTP_STATUS_OK,
        'headers': HEADERS_JSON,
        'body': body
    }


def response_400() -> dict:
    return {
        'statusCode': 400,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Missing doubt_id in path parameters'})
    }


def response_404() -> dict:
    return {
        'statusCode': HTTP_STATUS_NOT_FOUND,
        'headers': HEADERS_JSON,
        'body': json.dumps({'error': 'Doubt not found'})
    }


def response_500() -> dict:
    return {
        'statusCode': HTTP_STATUS_INTERNAL_SERVER_ERROR,
        'headers': HEADERS_JSON,
        'body': json.dumps({'error': 'Internal Server Error'})
    }


def client_error_response(ce) -> dict:
    return {
        'statusCode': HTTP_STATUS_INTERNAL_SERVER_ERROR,
        'headers': HEADERS_JSON,
        'body': json.dumps({'error': f'Internal Server Error: {ce.response["Error"]["Message"]}'})
    }
