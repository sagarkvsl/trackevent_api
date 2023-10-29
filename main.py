from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track_event', methods=['POST'])
def track_event():
    ma_key = request.form['ma_key']
    email = request.form['email']
    event = request.form['event']

    eventdata_str = request.form.get('eventdata', '')  # Get the eventdata string, default to empty string

    if eventdata_str:
        try:
            eventdata = json.loads(eventdata_str)  # Attempt to parse JSON if the field is not empty
        except json.JSONDecodeError as e:
            return f"Invalid JSON in eventdata: {str(e)}", 400
    else:
        eventdata = None  # Set eventdata to None if the field is empty

    # Make a POST request to the API with the provided ma-key, email, event, and eventdata
    url = 'https://in-automate.brevo.com/api/v2/trackEvent'
    headers = {
        'ma-key': ma_key,
        'Content-Type': 'application/json',
        'accept': 'application/json',
    }
    data = {
        "email": email,
        "event": event,
        "eventdata": eventdata,
        "properties": {"additionalProp": "string"}
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        return "Event tracked successfully"
    else:
        return f"Event tracking failed with status code: {response.status_code}", 400

if __name__ == '__main__':
    app.run(debug=True)
