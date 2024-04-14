import os
import json
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
# Get the DynamoDB table
table = dynamodb.Table(os.environ['TRANSLATIONS_TABLE_NAME'])


def lambda_handler(event, context):
    # Parse the request body
    body = json.loads(event['body'])

    # Get the English and French translations from the request body
    english_translation = body.get('english', '')
    french_translation = body.get('french', '')

    # Scan the DynamoDB table to check if the provided translation matches
    try:
        response = table.scan(
            FilterExpression="english = :english_translation",
            ExpressionAttributeValues={":english_translation": english_translation}
        )
        items = response.get('Items')
        if items:
            # Check if any item in the result matches the provided French translation
            for item in items:
                if item.get('french') == french_translation:
                    # If the translation matches, return a successful response
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'correct': True})
                    }
        # If no matching translation is found, return the correct translation
        correct_translation = items[0].get('french') if items else None
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
