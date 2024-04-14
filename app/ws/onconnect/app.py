import json


def lambda_handler(event, context):
    """"
    Respond to websocket onconnect event
    """
    return {
        "statusCode": 200,
        "body": "Connected."
    }


