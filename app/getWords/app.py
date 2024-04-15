import os
import json
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
category_words_table = dynamodb.Table(os.environ['CATEGORIESWORDS_TABLE_NAME'])
translations_table = dynamodb.Table(os.environ['TRANSLATIONS_TABLE_NAME'])

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        # Parse the request body
        body = json.loads(event['body'])

        # Get the English and French translations from the request body
        category_name = body.get('category', '')['categoryName']
        print(category_name)

    try:
        # Fetch words for the category from the category_words_table
        response_category_words = category_words_table.query(
            KeyConditionExpression='categoryName = :category_name',
            ExpressionAttributeValues={':category_name': category_name}
        )
        words = response_category_words.get('Items', [])
        print(words)
        # Fetch English and French translations for each word from the translations_table
        translated_words = []
        for word in words:
            # Query translations table for English and French translations based on 'word_id'
            response_translations = translations_table.get_item(
                Key={'hash': word['word']}
            )
            # print(response_translations)
            translation_item = response_translations.get('Item', [])
            print(translation_item)
            # Construct dictionary with word and its translations
            if translation_item:
                translated_word = {
                    'word': translation_item['word'],
                    'translations': translation_item['translation']
                }
                translated_words.append(translated_word)
        print(translated_words)
        # Construct the response
        response_body = {
            'category': category_name,
            'words': translated_words
        }
        # Add CORS headers to allow cross-origin requests
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_body)
        }
    except Exception as e:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
