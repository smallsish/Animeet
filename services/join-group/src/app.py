import os
import socket
import json
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS

if os.environ.get('stage') == 'production-k8s':
    GROUPS_SERVICE_URL = os.environ.get('groups_service_url_internal')
    USERS_SERVICE_URL = os.environ.get('users_service_url_internal')
    EVENTS_SERVICE_URL = os.environ.get('events_service_url_internal')
    NOTIFICATIONS_SERVICE_URL = os.environ.get(
        'notifications_service_url_internal')
else:
    GROUPS_SERVICE_URL = 'http://groups:5000'
    USERS_SERVICE_URL = 'http://users:5000'
    EVENTS_SERVICE_URL = 'http://events:5000'
    NOTIFICATIONS_SERVICE_URL = 'http://notifications:5000'


app = Flask(__name__)

CORS(app)


def send_notification(email, subject, message):
    # Print to show whether notification succeeded
    print(requests.post(
        NOTIFICATIONS_SERVICE_URL + '/publish-join-notification',
        data=json.dumps({
            "email": email,
            "subject": subject,
            "body": message
        }),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    ).text)


@app.route("/health")
def health_check():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return jsonify(
            {
                "message": "Service is healthy.",
                "service:": "join-group",
                "ip_address": local_ip
            }
    ), 200


# Join a group (POST request with user_id and group_id)
@app.route('/join-group/<int:group_id>', methods=['POST'])
def join_group(group_id):
    user_id = request.json.get('user_id')
    event_id = request.json.get('event_id')

    user_response = requests.get(USERS_SERVICE_URL +
                                 '/users/' + str(user_id))
    if user_response.status_code != 200:
        return jsonify(
            {
                "message": "Could not fetch user data."
            }
        ), 400

    # Check if there are event slots left, disallow joining if 0
    event_response = requests.get(EVENTS_SERVICE_URL
                                  + '/events/' + str(event_id))
    if event_response.status_code == 200:
        if event_response.json()['data']['slots_left'] <= 0:
            return jsonify(
                {
                    "message": "Unable to join group, event is out of slots."
                }
            ), 400
    else:  # error retrieving event detail
        return jsonify(event_response.json()), event_response.status_code

    # Attempt to join group
    join_group_response = requests.post(
        GROUPS_SERVICE_URL + '/groups/' + str(group_id),
        data=json.dumps({
            "user_id": user_id
        }),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )

    if join_group_response.status_code == 200:
        # Notify all group members
        for member_id in join_group_response.json()['data']['members']:
            # Get emails from users service
            if member_id != user_id:  # No need to fetch for same user id
                member_response = requests.get(USERS_SERVICE_URL +
                                               '/users/' + str(member_id))
            else:
                member_response = user_response

            if member_response.status_code == 201:
                if member_id == user_id:
                    send_notification(user_response.json()['email'],
                                      "Group join success",
                                      "You have joined a group!")
                else:
                    # send notification about user joining group
                    send_notification(member_response.json()['email'],
                                      "Update in your event " +
                                      event_response.json()['data']
                                      ['event_name'],
                                      member_response.json()['user']
                                      ['username'] +
                                      " has joined your group.")
            else:  # Log by printing to console
                print(member_response.text)

    return jsonify(join_group_response.json()), join_group_response.status_code


# Leave a group (DELETE request with user_id and group_id)
@app.route('/leave-group/<int:group_id>/<int:user_id>', methods=['DELETE'])
def leave_group(group_id, user_id):
    leave_response = requests.delete(
        GROUPS_SERVICE_URL + '/groups/' + str(group_id) +
        '/users/' + str(user_id),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    # Removed sending email on leave as it gets too spammy

    return jsonify(leave_response.json()), leave_response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
