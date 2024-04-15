import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USERS_TABLE_NAME'])


def lambda_handler(event, context):
    body = json.loads(event['body'])
    email = body['email']
    elo = body['elo']

    # Insert into DynamoDB
    try:
        # update item with new elo
        response = table.get_item(Key={'email': email})
        item = response.get('Item')
        item['elo'] = item['elo'] + elo
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'ELO updated'}),
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
