import os
import json
import boto3
from urllib.parse import parse_qs


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USERS_TABLE_NAME'])


def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        body = parse_qs(event['body'])
        username = body['username'][0]
        password = body['password'][0]

        # Insert into DynamoDB
        try:
            table.put_item(
                Item={
                    'username': username,
                    'password': password
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Registration successful'})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }