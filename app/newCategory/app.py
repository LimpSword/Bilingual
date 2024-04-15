import hashlib
import os
import json
import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')


def table_exists(table_name):
    existing_tables = dynamodb.meta.client.list_tables()['TableNames']
    print(table_name, existing_tables, table_name in existing_tables)
    return table_name in existing_tables


def create_categories_table():
    categories_table_name = os.environ['CATEGORIES_TABLE_NAME']
    if not table_exists(categories_table_name):
        try:
            dynamodb.create_table(
                TableName=categories_table_name,
                KeySchema=[
                    {
                        'AttributeName': 'categoryName',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'categoryName',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,  # Adjust as needed
                    'WriteCapacityUnits': 5  # Adjust as needed
                }
            )
        except Exception as e:
            print(e)


def create_category_words_table():
    category_words_table_name = os.environ['CATEGORIESWORDS_TABLE_NAME']
    if not table_exists(category_words_table_name):
        try:
            dynamodb.create_table(
                TableName=category_words_table_name,
                KeySchema=[
                    {
                        'AttributeName': 'categoryName',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'word',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'categoryName',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'word',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,  # Adjust as needed
                    'WriteCapacityUnits': 5  # Adjust as needed
                }
            )
        except Exception as e:
            print(e)


def create_translation_table():
    category_words_table_name = os.environ['TRANSLATIONS_TABLE_NAME']
    if not table_exists(category_words_table_name):
        try:
            dynamodb.create_table(
                TableName=category_words_table_name,
                KeySchema=[
                    {
                        'AttributeName': 'hash',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'hash',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
        except Exception as e:
            print(e)


def create_tables():
    create_categories_table()
    create_category_words_table()
    create_translation_table()

def generate_hash(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

def add_word_to_translations_table(word, translation):
    try:
        translations_table_name = os.environ['TRANSLATIONS_TABLE_NAME']
        translations_table = dynamodb.Table(translations_table_name)
        hash_value = generate_hash(word+translation)
        print(word+translation, hash_value)
        translations_table.put_item(
            Item={
                'hash': str(hash_value),
                'word': word,
                'translation': translation
            }
        )
        return hash_value
    except Exception as e:
        print(e)

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        try:
            # Create tables if they don't exist
            create_tables()
            body = json.loads(event['body'])
            category_name = body['categoryName']
            words = body['words']

            print(category_name, words)

            # Insert category data into Categories table
            try:
                categories_table_name = os.environ['CATEGORIES_TABLE_NAME']
                categories_table = dynamodb.Table(categories_table_name)
                categories_table.put_item(
                    Item={
                        'categoryName': category_name,
                    }
                )
            except Exception as e:
                print(e)

            # Insert words into CategoryWords table
            category_words_table_name = os.environ['CATEGORIESWORDS_TABLE_NAME']
            category_words_table = dynamodb.Table(category_words_table_name)
            with category_words_table.batch_writer() as batch:
                for word in words:
                    print(word)
                    hash_val = add_word_to_translations_table(word['word'], word['translation'])
                    print(hash_val)
                    try:
                        category_words_table.put_item(
                            Item={
                                'categoryName': category_name,
                                'word': str(hash_val)
                            }
                        )
                    except Exception as e:
                        print(e)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Category created successfully'})
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
