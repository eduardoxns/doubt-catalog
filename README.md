# Doubt Catalog

_**Project Status: In Progress...**_

Welcome to the Doubt Catalog API, a serverless RESTful service designed for managing questions and answers.

This API allows you to:

- [x] **Create a new doubt**: Endpoint to create a new doubt.
- [x] **Get the doubts**: Retrieve a list of doubts.
- [x] **Delete the doubts**: Remove a doubt.
- [x] **Edit a doubt**: Modify an existing doubt.
- [x] **Create a new answer from doubt**: Add a new answer to a doubt.
- [x] **Get the answers from a doubt**: Retrieve answers associated with a doubt.
- [x] **Delete the answers from a doubt**: Remove an answer from a doubt.

Explore the documentation below to learn how to interact with the API.

# REST API

The REST API to the example app is described below.

### Endpoints:

`POST - https://m1xcjzho6f.execute-api.sa-east-1.amazonaws.com/dev/doubts`: Create a new doubt.

`GET - https://m1xcjzho6f.execute-api.sa-east-1.amazonaws.com/dev/doubts`: Retrieve a list of doubts.

`GET - https://m1xcjzho6f.execute-api.sa-east-1.amazonaws.com/dev/doubts/{doubt_id}`: Get details of a specific doubt.

`PUT - https://m1xcjzho6f.execute-api.sa-east-1.amazonaws.com/dev/doubts/{doubt_id}`: Edit an existing doubt.

`DELETE - https://m1xcjzho6f.execute-api.sa-east-1.amazonaws.com/dev/doubts/{doubt_id}`: Delete a doubt.

`POST - https://m1xcjzho6f.execute-api.sa-east-1.amazonaws.com/dev/doubts/{doubt_id}/answers`: Add a new answer to a doubt.

`GET - https://m1xcjzho6f.execute-api.sa-east-1.amazonaws.com/dev/doubts/{doubt_id}/answers`: Retrieve answers associated with a doubt.

`GET - https://m1xcjzho6f.execute-api.sa-east-1.amazonaws.com/dev/doubts/{doubt_id}/answers/{answer_id}`: Get details of a specific answer.

`DELETE - https://m1xcjzho6f.execute-api.sa-east-1.amazonaws.com/dev/doubts/{doubt_id}/answers/{answer_id}`: Remove an answer.

### Response Format:

All responses are in JSON format.

### HTTP Status Codes:

* `200 OK`: Successful operation.
* `400 Bad Request`: Invalid request.
* `404 Not Found`: Resource not found.
* `500 Internal Server Error`: Unexpected server error.
