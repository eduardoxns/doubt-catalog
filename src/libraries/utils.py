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
