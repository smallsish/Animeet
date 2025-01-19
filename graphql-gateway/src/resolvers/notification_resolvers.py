import requests
from ..config import NOTIFICATIONS_SERVICE_URL

def resolve_health_check(_, info):
    response = requests.get(f"{NOTIFICATIONS_SERVICE_URL}/health")
    return response.json()

def resolve_publish_notification(_, info, user_id, event_id, user_name, event_name, price, email):
    payload = {
        "user_id": user_id,
        "event_id": event_id,
        "user_name": user_name,
        "event_name": event_name,
        "price": price,
        "email": email
    }

    try:
        response = requests.post(f"{NOTIFICATIONS_SERVICE_URL}/publish-notification", json=payload)
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            return {
                "message": data.get("message", "Notification sent successfully."),
                "user_id": user_id,
                "event_id": event_id,
                "user_name": user_name,
                "event_name": event_name,
                "price": f"${price / 100:.2f}",  # Converting price from cents to formatted dollars
                "email": email,
                "error": None
            }
        else:
            error_data = response.json() if response.content else {}
            return {
                "message": error_data.get("message", "Failed to send notification."),
                "user_id": user_id,
                "event_id": event_id,
                "user_name": user_name,
                "event_name": event_name,
                "price": f"${price / 100:.2f}",
                "email": email,
                "error": error_data.get("error")
            }
    except Exception as e:
        return {
            "message": "An unexpected error occurred while sending the notification.",
            "user_id": user_id,
            "event_id": event_id,
            "user_name": user_name,
            "event_name": event_name,
            "price": f"${price / 100:.2f}",
            "email": email,
            "error": str(e)
        }
