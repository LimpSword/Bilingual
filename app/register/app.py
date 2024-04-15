import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USERS_TABLE_NAME'])


# # Create table if it doesn't exist
# if os.environ['USERS_TABLE_NAME'] not in dynamodb.meta.client.list_tables()['TableNames']:
#     # We only need to define the basic schema here (at least the key)
#     dynamodb.create_table(
#         TableName=os.environ['USERS_TABLE_NAME'],
#         KeySchema=[
#             {
#                 'AttributeName': 'email',
#                 'KeyType': 'HASH'
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'email',
#                 'AttributeType': 'S'
#             }
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 5,
#             'WriteCapacityUnits': 5
#         }
#
#     )


def lambda_handler(event, context):
    body = json.loads(event['body'])
    username = body['username']
    email = body['email']
    password = body['password']

    # Insert into DynamoDB
    try:
        session_id = os.urandom(16).hex()
        table.put_item(
            Item={
                'email': email,
                'username': username,
                'password': password,
                'authorized_sessions': [session_id],
                'elo': 1000,
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'session_id': session_id, "username": username, "email": email}),
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)}),
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }
