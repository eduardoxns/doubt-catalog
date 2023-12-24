# Doubt Catalog

_**Project Status: In Progress**_

Welcome to the Doubt Catalog API, a serverless RESTful service designed for managing questions and answers.

This API allows you to:

* Retrieve a list of doubts
* Get details of a specific doubt
* Add a new doubt

Explore the documentation below to learn how to interact with the API.

# REST API

The REST API to the example app is described below.


## Create a new Doubt

### Request

`POST /doubts`

    curl --location --request POST 'https://l6xuqzyeal.execute-api.sa-east-1.amazonaws.com/dev/doubts' \ --header 'Content-Type: application/json' \ --data '{ "title": "test", "description": "test"}'

### Response

    {
        "id": "b1475efc-a2af-11ee-b901-3234e66b7578",
        "title": "test",
        "description": "test",
        "answers": 0,
        "created_at": "2023-12-24T22:56:37.228593",
        "updated_at": "2023-12-24T22:56:37.228610"
    }


## Get list of Doubts

### Request

`GET /doubts`

    curl --location 'https://l6xuqzyeal.execute-api.sa-east-1.amazonaws.com/dev/doubts'

### Response

    [
        {
            "updated_at": "2023-12-24T21:42:30.475203",
            "created_at": "2023-12-24T21:42:30.475182",
            "answers": 0.0,
            "description": "test",
            "id": "56cea610-a2a5-11ee-85ec-d639ea083cf1",
            "title": "test"
        },
        ...
    ]


## Get a specific Doubt

### Request

`GET /doubts/{id}`

    curl --location 'https://l6xuqzyeal.execute-api.sa-east-1.amazonaws.com/dev/doubts/b1475efc-a2af-11ee-b901-3234e66b7578'

### Response

    {
        "updated_at": "2023-12-24T22:56:37.228610",
        "created_at": "2023-12-24T22:56:37.228593",
        "answers": 0.0,
        "description": "test",
        "id": "b1475efc-a2af-11ee-b901-3234e66b7578",
        "title": "test"
    }


## Delete a Doubt

### Request

`DELETE /doubts/{id}`

    curl --location --request DELETE 'https://l6xuqzyeal.execute-api.sa-east-1.amazonaws.com/dev/doubts/56cea610-a2a5-11ee-85ec-d639ea083cf1'

### Response

    {
        "message": "Doubt 56cea610-a2a5-11ee-85ec-d639ea083cf1 deleted successfully"
    }


## Edit a Doubt

### Request

`PUT /doubts/{id}`

    curl --location --request PUT 'https://l6xuqzyeal.execute-api.sa-east-1.amazonaws.com/dev/doubts/0cb70b8c-9759-11ee-88cb-76dcdbe8e31a' \ --header 'Content-Type: application/json' \ --data '{"title": "test", "description": "test"}'

### Response

    {
        "updated_at": "2023-12-24T23:08:44.939027",
        "created_at": "2023-12-10T12:38:41.627073",
        "answers": 0.0,
        "description": "test",
        "id": "0cb70b8c-9759-11ee-88cb-76dcdbe8e31a",
        "title": "test"
    }