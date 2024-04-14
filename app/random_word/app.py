import os
import json
import boto3
import random

dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
table = dynamodb.Table(os.environ['TRANSLATIONS_TABLE_NAME'])

def lambda_handler(event, context):

    if event['httpMethod'] == 'GET':
        # get a random word from the database
        try:
            print("random_word")
            response = table.scan()
            items = response['Items']
            word = random.choice(items)
            print(word)
            english = word['english']
            french = word['french']
            return {
                'statusCode': 200,
                'body': json.dumps({'english': english, 'french': french})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }

    # elif event['httpMethod'] == 'POST' and event['path'] == '/check-translation':
    #     # check if the submitted translation is correct
    #     body = json.loads(event['body'])
    #     english = body['english']
    #     translation = body['translation']
    #     response = table.get_item(Key={'english': english})
    #     item = response['Item']
    #     correct_translation = item['french']
    #     is_correct = translation.lower() == correct_translation.lower()
    #     return {
    #         'statusCode': 200,
    #         'body': json.dumps({'is_correct': is_correct})
    #     }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Not found'})
        }

