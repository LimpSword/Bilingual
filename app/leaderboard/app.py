import os
import json
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
table = dynamodb.Table(os.environ['USERS_TABLE_NAME'])


def lambda_handler(event, context):
    # Return all users sorted by elo
    if event['httpMethod'] == 'GET':
        try:
            response = table.scan()
            items = response.get('Items')
            items.sort(key=lambda x: x['elo'], reverse=True)

            safe_items = []
            for item in items:
                safe_item = {'username': item['username'], 'elo': int(item['elo'])}
                safe_items.append(safe_item)

            return {
                'statusCode': 200,
                'body': json.dumps(safe_items)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }
