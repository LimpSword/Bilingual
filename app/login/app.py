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

        try:
            response = table.get_item(Key={'username': username})
            item = response.get('Item')
            if item and item['password'] == password:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Login successful'})
                }
            else:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'message': 'Login failed'})
                }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }
