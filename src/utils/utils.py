def http_response(data, status_code=422, dump=True, sort=True):
    if dump:
        data = dumps(data, cls=DecimalEncoder, sort_keys=sort)

    return {
        "statusCode": status_code,
        "body": data,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
    }