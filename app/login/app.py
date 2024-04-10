import os
import json
import boto3


dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
table = dynamodb.Table(os.environ['USERS_TABLE_NAME'])


def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        email = body['email']
        password = body['password']

        try:
            response = table.get_item(Key={'email': email})
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
