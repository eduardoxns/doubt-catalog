import json
import logging
from botocore.exceptions import ClientError

from infra.dynamodb.dynamodb import dynamodb
from src.libraries.exceptions import HttpResponses

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = 'doubt_catalog'


def delete_item(doubt_id, specific_answer_index):
    return {
        'Key': {'id': doubt_id},
        'UpdateExpression': f'REMOVE answers[{specific_answer_index}]'
    }


def lambda_handler(event, context):
    params = event.get("pathParameters", {})
    doubt_id = params.get("doubt_id")
    answer_id = params.get("answer_id")

    if not doubt_id or not answer_id:
        return HttpResponses.http_response_400("Missing doubt_id or answer_id in path parameters!")

    try:
        response = dynamodb.Table(TABLE_NAME).get_item(Key={'id': doubt_id})
        item = response.get("Item")

        if not item:
            return HttpResponses.http_response_404(f"Doubt with id {doubt_id} does not exist!")

        answers = item.get("answers", [])
        specific_answer_index = next((index for index, answer in enumerate(answers) if answer.get("id") == answer_id), None)

        if specific_answer_index is not None:
            dynamodb.Table(TABLE_NAME).update_item(**delete_item(doubt_id, specific_answer_index))

            body = {'message': f'Answer {answer_id} deleted successfully from doubt {doubt_id}!'}
            return HttpResponses.http_response_200(json.dumps(body))
        return HttpResponses.http_response_404(f'Answer {answer_id} not found in doubt {doubt_id}!')

    except ClientError as ce:
        error_message = ce.response.get("Error", {}).get("Message", "Unknown Error")
        logger.exception(f'Error deleting answer: {error_message}')
        return HttpResponses.http_client_error_response(ce)

    except Exception as e:
        logger.exception(f'Unexpected error deleting answer: {e}')
        return HttpResponses.http_response_500()
