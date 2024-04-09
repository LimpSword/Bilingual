import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USERS_TABLE_NAME'])


def lambda_handler(event, context):
    html = """
    <html>
        <head>
            <title>Register</title>
        </head>
        <body>
            <h1>Register</h1>
            <form action="/register" method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Register</button>
            </form>
            <a href="/login">Login</a>
        </body>
    </html>
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html
    }
