import requests
from ..config import MAKE_A_PAYMENT_SERVICE_URL

def resolve_health_check(_, info):
    response = requests.get(f"{MAKE_A_PAYMENT_SERVICE_URL}/health")
    return response.json()

def resolve_make_a_payment(_, info, user_id, group_id, event_id):
    payload = {
        "user_id": user_id,
        "group_id": group_id,
        "event_id": event_id
    }

    try:
        response = requests.post(f"{MAKE_A_PAYMENT_SERVICE_URL}/make-a-payment", json=payload)
        if response.status_code == 201:
            # data = response.json().get("data")
            data = response.json()
            return {
                "status": "success",
                "url": data.get("url"),
                "event_name": data.get("event_name"),
                "price": data.get("price"),
                "message": data.get("message", "Payment created successfully."),
                "error": None
            }
        else:
            error_data = response.json() if response.content else {}
            return {
                "status": "failure",
                "url": None,
                "event_name": None,
                "price": None,
                "message": error_data.get("message", "An error occurred during the payment process."),
                "error": error_data.get("error")
            }
    except Exception as e:
        return {
            "status": "failure",
            "url": None,
            "event_name": None,
            "price": None,
            "message": "An unexpected error occurred during the payment process.",
            "error": str(e)
        }
