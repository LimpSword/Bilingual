import os
import json
import boto3
import random

dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
translations_table = dynamodb.Table(os.environ['TRANSLATIONS_TABLE_NAME'])
category_words_table = dynamodb.Table(os.environ['CATEGORIESWORDS_TABLE_NAME'])

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        # Parse the request body
        body = json.loads(event['body'])
        # Get the English and French translations from the request body
        category_name = body.get('category', '')

        try:
            if category_name != 'all':
                # Fetch words for the category from the category_words_table
                print("category_name: ", category_name)
                response_category_words = category_words_table.query(
                    KeyConditionExpression='categoryName = :category_name',
                    ExpressionAttributeValues={':category_name': category_name}
                )
                words = response_category_words.get('Items', [])
            else:
                print("category_name is empty")
                response_category_words = category_words_table.scan()
                words = response_category_words.get('Items', [])

            if words:
                print(words)
                word = random.choice(words)
                print(word)
                try:
                    response_translations = translations_table.get_item(
                        Key={'hash': word['word']}
                    )
                    translation_item = response_translations.get('Item', None)
                except Exception as e:
                    print(str(e))

                print(translation_item)
                if translation_item:
                    translated_word = {
                        'word': translation_item['word'],
                        'translations': translation_item['translation']
                    }
                    print(translated_word)
                    headers = {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                        'Access-Control-Allow-Headers': 'Content-Type'
                    }
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps({'english': translated_word['word'], 'french': translated_word['translations']})
                    }

            # If no word found or translation item is None
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps('Word not found')
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


