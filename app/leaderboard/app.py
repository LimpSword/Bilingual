import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USERS_TABLE_NAME'])


def lambda_handler(event, context):
    html = """
    <html>
        <head>
            <title>Leaderboard</title>
        </head>
        <body>
            <h1>Leaderboard</h1>
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
