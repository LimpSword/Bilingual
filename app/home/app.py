def lambda_handler(event, context):
    html = """
    <html>
        <head>
            <title>Home</title>
        </head>
        <body>
            <h1>Welcome</h1>
            <a href="/login">Login</a>
            <a href="/register">Register</a>
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