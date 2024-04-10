import os
import json
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
table = dynamodb.Table(os.environ['USERS_TABLE_NAME'])


def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        username = body['username'][0]
        email = body['email'][0]
        password = body['password'][0]

        # Insert into DynamoDB
        try:
            table.put_item(
                Item={
                    'email': email,
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
