import csv
import hashlib
import os
import re
import unicodedata

import boto3

# Set up DynamoDB client


os.environ['TRANSLATIONS_TABLE_NAME'] = 'TranslationsTable'

dynamodb = boto3.resource('dynamodb', endpoint_url='http://172.17.0.1:8000')
table_name = os.environ['TRANSLATIONS_TABLE_NAME']

# Check if the table exists, and create it if it doesn't
if table_name not in dynamodb.meta.client.list_tables()['TableNames']:
    dynamodb.create_table(
        TableName=table_name,
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

# Connect to the table
table = dynamodb.Table(table_name)


def removeUseless(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    text = re.sub(r"[^a-zA-Z0-9àáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'\s]", '', text)
    return text.strip()

# Parse the CSV file
with open('../archive/en-fr.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)  # Skip the header row
    for row in reader:
        english = row[0].strip()
        french = row[1].strip()
        english = removeUseless(english)
        french = removeUseless(french)
        # Only insert English sentences that are less than 30 characters long
        if len(english) < 30:
            hash_value = hashlib.sha256(english.encode('utf-8')).hexdigest()

            # Insert the translation into the table
            try:
                table.put_item(
                    Item={
                        'hash': hash_value,
                        'english': english,
                        'french': french,
                    }
                )
            except Exception as e:
                print(f"Error inserting translation for English sentence '{english}': {e}")
