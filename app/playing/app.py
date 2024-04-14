import os
import json
import boto3
import random

dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
table = dynamodb.Table(os.environ['TRANSLATIONS_TABLE_NAME'])

def lambda_handler(event, context):
    global table
    if event['httpMethod'] == 'POST':
        pass
        # Handle registration logic here
        # ...
    elif event['httpMethod'] == 'GET' and event['path'] == '/play':
        # Get a random word from the database
        response = table.scan(
            ProjectionExpression='english, french',
            FilterExpression='size(english) <= 30'
        )
        items = response['Items']
        print("play")
        if items:
            word = random.choice(items)
            print(word)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'english': word['english'],
                    'french': word['french']
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No words found'})
            }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Not found'})
        }
    import json
    import random
    import boto3

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TRANSLATIONS_TABLE_NAME'])

    def lambda_handler(event, context):
        # handle registration logic
        if event['httpMethod'] == 'GET' and event['path'] == '/random-word':
            # get a random word from the database
            response = table.scan()
            items = response['Items']
            word = random.choice(items)
            english = word['english']
            french = word['french']
            return {
                'statusCode': 200,
                'body': json.dumps({'english': english, 'french': french})
            }
        elif event['httpMethod'] == 'POST' and event['path'] == '/check-translation':
            # check if the submitted translation is correct
            body = json.loads(event['body'])
            english = body['english']
            translation = body['translation']
            response = table.get_item(Key={'english': english})
            item = response['Item']
            correct_translation = item['french']
            is_correct = translation.lower() == correct_translation.lower()
            return {
                'statusCode': 200,
                'body': json.dumps({'is_correct': is_correct})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Not found'})
            }

