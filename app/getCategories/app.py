import os
import json
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
categories_table = dynamodb.Table(os.environ['CATEGORIES_TABLE_NAME'])

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        try:
            response = categories_table.scan()
            items = response.get('Items')
            print(items)
            if not items:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Category not found'})
                }

            return {
                'statusCode': 200,
                'body': json.dumps(items)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Not found'})
        }
