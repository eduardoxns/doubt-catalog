import logging


class MissingBodyError(Exception):
    def __init__(self, message="Request body is missing or empty"):
        self.message = message
        super().__init__(self.message)


def verify_if_body_exist(data):
    if 'body' not in data or not data['body']:
        raise MissingBodyError()


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def reorder_json(input_json, answer=False):
    if not isinstance(input_json, dict):
        return input_json

    if answer:
        ordered_keys = ["id", "answer", "created_at"]
    else:
        ordered_keys = ["id", "title", "description", "answers", "updated_at", "created_at"]

    reordered_json = {key: input_json[key] for key in ordered_keys if key in input_json}
    for key in input_json.keys():
        if key not in ordered_keys:
            reordered_json[key] = input_json[key]
    return reordered_json
