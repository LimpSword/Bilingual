from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


def handler(event, context):
    return {"statusCode": 200, "body": hello()}


if __name__ == "__main__":
    app.run()
