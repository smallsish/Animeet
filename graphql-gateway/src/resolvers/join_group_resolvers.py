import requests
from ..config import JOIN_GROUP_SERVICE_URL

#.

def resolve_health_check(_, info):
    response = requests.get(f"{JOIN_GROUP_SERVICE_URL}/health")
    return response.json()

def resolve_join_group_composite(_, info, user_id, group_id, event_id):
    payload = {
        "user_id": user_id,
        "event_id": event_id
    }
    try:
        response = requests.post(f"{JOIN_GROUP_SERVICE_URL}/join-group/{group_id}", json=payload)
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            data = response_data.get("data")
            return {
                "message": response_data.get("message", "User joined group successfully."),
                "error": None,
                "data": {
                    "joined": data.get("joined"),
                    "group_id": group_id,
                    "user_id": user_id,
                    "role": data.get("role", None),
                    "status": data.get("status", None),
                    "members": data.get("members", [])
                }
            }
        else:
            error_message = response.json().get("message", "Failed to join group.")
            return {
                "message": "Failed to join group.",
                "error": error_message,
                "data": None
            }
    except Exception as e:
        return {
            "message": "Failed to join group due to an exception.",
            "error": str(e),
            "data": None
        }

def resolve_leave_group(_, info, user_id, group_id, event_id):
    payload = {
        "user_id": user_id,
        "event_id": event_id
    }
    try:
        response = requests.delete(f"{JOIN_GROUP_SERVICE_URL}/leave-group/{group_id}/{user_id}", json=payload)
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            return {
                "message": response_data.get("message", "User left group successfully."),
                "error": None,
                "data": {
                    "group_id": group_id,
                    "user_id": user_id,
                    "members": response_data.get("data").get("members")
                }
            }
        else:
            error_message = response.json().get("message", "Failed to leave group.")
            return {
                "message": "Failed to leave group.",
                "error": error_message,
                "data": None
            }
    except Exception as e:
        return {
            "message": "Failed to leave group due to an exception.",
            "error": str(e),
            "data": None
        }
