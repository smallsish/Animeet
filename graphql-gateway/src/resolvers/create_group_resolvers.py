from flask import jsonify, make_response
import requests
from ..config import CREATE_GROUP_SERVICE_URL

def resolve_health_check(_, info):
    response = requests.get(f"{CREATE_GROUP_SERVICE_URL}/health")
    return response.json()

def resolve_create_group_composite(_, info, event_id, user_id, name, max_capacity, description):
    # Prepare the payload
    payload = {
        "event_id": event_id,
        "user_id": user_id,
        "name": name,
        "max_capacity": max_capacity,
        "description": description
    }

    try:
        # Call the /create-group composite endpoint
        response = requests.post(f"{CREATE_GROUP_SERVICE_URL}/create-group", json=payload)

        # Check if the response was successful
        if response.status_code == 201:
            response_data = response.json()
            data = response_data.get("data", {})
            return {
                "message": response_data.get("message", "Group created successfully."),
                "error": None,
                "data": {
                    "group_data": data.get("group_data", {}),
                    "event_data": data.get("event_data", {})
                }
            }
        # else:
        #     error_message = response.json().get("message", "Unable to create group.")
        #     return make_response(jsonify({
        #         "message": "Failed to create group.",
        #         "error": error_message,
        #         "data": None
        #     }), 404)
        else:
            error_message = response.json().get("error", "Unable to create group.")
            return {
                "message": "Failed to create group.",
                "error": error_message,
                "data": None
            }

    except Exception as e:
        # Handle any exceptions that occur during the request
        return {
            "message": "Failed to create group due to an exception.",
            "error": str(e),
            "data": None
        }