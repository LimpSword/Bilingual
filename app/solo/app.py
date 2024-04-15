import json
from flask import Flask, request
from flask_cors import CORS  # Import the CORS extension

from automatic_translation import all_details,lg,lg_abvr

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the Flask app

@app.route('/moreTrad', methods=['POST'])
def more_trad():
    if request.method == 'POST':
        body = request.json

        # Get the English and French translations from the request body
        word = body.get('word', '')
        origin_language = body.get('origin_language', '')
        destination_language = body.get('destination_language', '')

        # Call your Python function with the provided parameters
        translations = all_details(lg_abvr[lg.index(origin_language)], lg_abvr[lg.index(destination_language)], word)
        print(translations)

        # Return the translations as a JSON response
        return json.dumps(translations), 200

    else:
        # Return a 404 Not Found response for other HTTP methods
        return json.dumps({'message': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
