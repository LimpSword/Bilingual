def lambda_handler(event, context):
    """"
    Respond to websocket ondisconnect event
    """
    return {
        "statusCode": 200,
        "body": "Disconnected."
    }


