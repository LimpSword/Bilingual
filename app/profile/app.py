import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USERS_TABLE_NAME'])


def lambda_handler(event, context):
    html = """
    <html>
        <head>
            <title>Profile</title>
        </head>
        <body>
            <h1>Profile</h1>
            <a href="/logout">Logout</a>
        </body>
    </html>
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html
    }
