import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
categories_table = dynamodb.Table(os.environ['CATEGORIES_TABLE_NAME'])
category_words_table = dynamodb.Table(os.environ['CATEGORY_WORDS_TABLE_NAME'])

def lambda_handler(event, context):
    category_name = event['pathParameters']['category_name']

    try:
        # Fetch category data
        response = categories_table.get_item(Key={'categoryName': category_name})
        category_data = response.get('Item')

        if not category_data:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Category not found'})
            }

        # Fetch words for the category
        response = category_words_table.query(
            KeyConditionExpression='categoryName = :category_name',
            ExpressionAttributeValues={':category_name': category_name}
        )
        words = response.get('Items', [])

        # Construct the response
        response_body = {
            'category': category_data,
            'words': words
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response_body)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
