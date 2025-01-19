import os
import socket
import json
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS

if os.environ.get('stage') == 'production-k8s':
    GROUPS_SERVICE_URL = os.environ.get('groups_service_url_internal')
    EVENTS_SERVICE_URL = os.environ.get('events_service_url_internal')
else:
    GROUPS_SERVICE_URL = 'http://groups:5000'
    EVENTS_SERVICE_URL = 'http://events:5000'

app = Flask(__name__)

CORS(app)


@app.route("/health")
def health_check():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return jsonify(
            {
                "message": "Service is healthy.",
                "service:": "create-group",
                "ip_address": local_ip
            }
    ), 200


@app.route("/create-group", methods=['POST'])
def create_group():
    data = request.get_json()

    # NEW: (1) Check available slots for event
    event_response = requests.get(EVENTS_SERVICE_URL
                                  + '/events/' + str(data['event_id']))
    # Error on Event service
    if event_response.status_code != 200:

        error_message = event_response.json().get('message', 'Unable to create group.')

        return jsonify(
            {
                "message": error_message,
                "error": "Failed to create group."
            }
        ), 500
    # Success on Event service, but insufficient slots
    elif event_response.json()['data']['slots_left'] < data['max_capacity']:
        return jsonify(
            {
                "message": "Unable to create group.",
                "error": "Event slots insufficient"
            }
        ), 400

    # (2) Create group
    group_response = requests.post(
        GROUPS_SERVICE_URL + '/groups',
        data=json.dumps({
            'event_id': data['event_id'],
            'user_id': data['user_id'],
            'name': data['name'],
            'max_capacity': data['max_capacity'],
            'description': data['description']
        }),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )

    # Error on Group service
    if group_response.status_code != 201:
        # Try to get the message from the response JSON
        try:
            error_message = group_response.json().get('message', 'Unable to create group.')
        except ValueError:
            # If response is not JSON, fall back to a default message
            error_message = 'Unable to create group.'

        return jsonify(
            {
                "message": error_message,
                "error": "Unable to create group record."
            }
        ), 500

    # Combine responses for the final output
    response_data = {
        "group_data": group_response.json()['data'],
        "event_data": event_response.json()['data']
    }

    return jsonify(
        {
            "message": "Group created.",
            "data": response_data
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
