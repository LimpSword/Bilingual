import os
import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
# Get the DynamoDB table
table = dynamodb.Table(os.environ['TRANSLATIONS_TABLE_NAME'])


def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        # Parse the request body
        body = json.loads(event['body'])

        # Get the English and French translations from the request body
        english_translation = body.get('english', '')
        french_translation = body.get('french', '')
        print(english_translation, french_translation)
        # Scan the DynamoDB table to check if the provided translation matches
        try:
            response = table.scan(
                FilterExpression="word = :english_translation",
                ExpressionAttributeValues={":english_translation": english_translation}
            )
            items = response.get('Items')
            print(items)
            if items:
                # Check if any item in the result matches the provided French translation
                for item in items:
                    print()
                    if item.get('translation') == french_translation:
                        # If the translation matches, return a successful response
                        return {
                            'statusCode': 200,
                            'body': json.dumps({'correct': True})
                        }
            # If no matching translation is found, return the correct translation
            correct_translation = items[0].get('translation') if items else None
            return {
                'statusCode': 200,
                'body': json.dumps({'correct': False, 'correctTranslation': correct_translation})
            }
        except Exception as e:
            # Return an error response if there's an exception
            return {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }
    else:
        # Return a 404 Not Found response for other HTTP methods
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Not found'})
        }
