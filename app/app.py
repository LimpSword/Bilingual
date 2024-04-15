from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


from flask import Flask, request, jsonify
from app.solo.automatic_translation import all_details

app = Flask(__name__)


@app.route('/translate', methods=['GET'])
def translate_word():
    try:
        word = request.args.get('word')
        origin_language = request.args.get('origin_language')
        destination_language = request.args.get('destination_language')

        # Call your Python function with the provided parameters
        translations = all_details(origin_language, destination_language, word)
        print(translations)
        # Return the translations as a JSON response
        return jsonify({'translations': translations}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


def handler(event, context):
    return {"statusCode": 200, "body": hello()}


if __name__ == "__main__":
    app.run()
