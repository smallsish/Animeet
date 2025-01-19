import requests
from ..config import EVENTS_SERVICE_URL

def resolve_health_check(_, info):
    response = requests.get(f"{EVENTS_SERVICE_URL}/health")
    return response.json()

def resolve_get_event(_, info, event_id):
    response = requests.get(f"{EVENTS_SERVICE_URL}/events/{event_id}")
    if response.status_code == 200:
        event_data = response.json()
        return {
            "message": "Event retrieved successfully.",
            "error": None,
            "data": event_data["data"]
        }
    else:
        error_message = response.json().get("message", "Failed to retrieve event.")
        return {
            "message": "Failed to retrieve event.",
            "error": error_message,
            "data": None
        }

def resolve_list_events(_, info):
    response = requests.get(f"{EVENTS_SERVICE_URL}/events")
    if response.status_code == 200:
        events_data = response.json()
        if "data" in events_data:
            events_list = [
                {
                    "event_id": event["event_id"],
                    "event_name": event["event_name"],
                    "venue": event["venue"],
                    "entry_fee": float(event["entry_fee"]),
                    "capacity": int(event["capacity"]),
                    "slots_left": int(event["slots_left"]),
                    "description": event["description"],
                    "time": event["time"]
                }
                for event in events_data["data"]["events"]  # Iterate over each event in the list
            ]
            return {
                "data": events_list,
                "message": "Events retrieved successfully."
            }
        else:
            return {
                "data": [],
                "message": "No events available."
            }
    else:
        error_message = response.json().get("message", "Failed to retrieve events.")
        return {
            "data": None,
            "message": error_message
        }


def resolve_create_event(_, info, name, venue, entry_fee, capacity, slots_left, description, time):
    payload = {
        "event_name": name,
        "venue": venue,
        "entry_fee": entry_fee,
        "capacity": capacity,
        "slots_left": slots_left,
        "description": description,
        "time": time
    }
    response = requests.post(f"{EVENTS_SERVICE_URL}/events", json=payload)
    if response.status_code == 201:
        event_data = response.json()
        return {
            "message": "Event created successfully.",
            "error": None,
            "data": event_data["data"]
        }
    else:
        error_message = response.json().get("message", "Failed to create event.")
        return {
            "message": "Failed to create event.",
            "error": error_message,
            "data": None
        }

def resolve_update_event_details(_, info, event_id, name=None, venue=None, entry_fee=None, capacity=None, slots_left=None, description=None, time=None):
    payload = {}
    if name is not None:
        payload["event_name"] = name
    if venue is not None:
        payload["venue"] = venue
    if entry_fee is not None:
        payload["entry_fee"] = entry_fee
    if capacity is not None:
        payload["capacity"] = capacity
    if slots_left is not None:
        payload["slots_left"] = slots_left
    if description is not None:
        payload["description"] = description
    if time is not None:
        payload["time"] = time

    response = requests.patch(f"{EVENTS_SERVICE_URL}/events/{event_id}", json=payload)
    if response.status_code == 200:
        updated_event_data = response.json()
        return {
            "message": "Event updated successfully.",
            "error": None,
            "data": updated_event_data["data"]
        }
    else:
        error_message = response.json().get("message", "Failed to update event.")
        return {
            "message": "Failed to update event.",
            "error": error_message,
            "data": None
        }

def resolve_update_event_slots(_, info, event_id, slots):
    payload = {
        "reserve": slots
    }
    response = requests.patch(f"{EVENTS_SERVICE_URL}/events/{event_id}", json=payload)
    if response.status_code == 200:
        updated_event_data = response.json()
        return {
            "message": "Event slots updated successfully.",
            "error": None,
            "data": updated_event_data["data"]
        }
    else:
        error_message = response.json().get("message", "Failed to update event slots.")
        return {
            "message": "Failed to update event slots.",
            "error": error_message,
            "data": None
        }

def resolve_delete_event(_, info, event_id):
    response = requests.delete(f"{EVENTS_SERVICE_URL}/events/{event_id}")
    if response.status_code == 200:
        return {
            "message": "Event deleted successfully.",
            "error": None,
            "data": {
                "event_id": event_id
            }
        }
    else:
        error_message = response.json().get("message", "Failed to delete event.")
        return {
            "message": "Failed to delete event.",
            "error": error_message,
            "data": None
        }
