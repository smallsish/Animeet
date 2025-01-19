import requests
import os
from dotenv import load_dotenv
from ..config import PAYMENTS_SERVICE_URL

load_dotenv()

def resolve_health_check(_, info):
    response = requests.get(f"{PAYMENTS_SERVICE_URL}/health")
    return response.json()

def resolve_create_checkout_session(_, info, user_id, group_id, event_id, event_name, price, amount):
    payload = {
        "user_id": user_id,
        "group_id": group_id,
        "event_id": event_id,
        "event_name": event_name,
        "price": price,
        "amount": amount
    }
    response = requests.post(f"{PAYMENTS_SERVICE_URL}/checkout-session", json=payload)
    # data = response.json().get("data")
    data = response.json()
    
    return {
        "session_id": data.get("session_id"),
        "url": data.get("url"),
        "status": data.get("status"),
        "message": data.get("message"),
        "error": data.get("error"),
        "event_name": event_name,
        "price": price
    }

def resolve_get_payment(_, info, user_id):
    response = requests.get(f"{PAYMENTS_SERVICE_URL}/payments/{user_id}")
    data = response.json()
    
    return {
        "data": data.get("data"),
        "message": data.get("message")
    }

def resolve_list_payments(_, info):
    response = requests.get(f"{PAYMENTS_SERVICE_URL}/payments")
    if response.status_code == 200:
        payments_data = response.json()
        if "data" in payments_data:
            # Transform the list of payments to match the Payment schema
            payments_list = [
                {
                    "payment_id": payment["payment_id"],
                    "user_id": payment["user_id"],
                    "group_id": payment["group_id"],
                    "date": payment["date"]
                }
                for payment in payments_data["data"]
            ]
            return {
                "data": payments_list,
                "message": "Payments retrieved successfully."
            }
        else:
            return {
                "data": [],
                "message": "No payments available."
            }
    else:
        error_message = response.json().get("message", "Failed to retrieve payments.")
        return {
            "data": None,
            "message": error_message
        }

def resolve_refund_payment(_, info, payment_id):
    payload = {"payment_id": payment_id}
    response = requests.post(f"{PAYMENTS_SERVICE_URL}/refund", json=payload)
    # data = response.json().get("data")
    data = response.json()

    return {
        "status": data.get("status"),
        "refund_id": data.get("refund_id"),
        "error": data.get("error")
    }

def resolve_delete_payment(_, info, payment_id):
    response = requests.delete(f"{PAYMENTS_SERVICE_URL}/payments/{payment_id}")
    # data = response.json().get("data")
    data = response.json()
    
    return {
        "message": data.get("message"),
        "error": data.get("error")
    }

def resolve_add_payment(_, info, payment_id, user_id, group_id, date):
    payload = {
        "payment_id": payment_id,
        "user_id": user_id,
        "group_id": group_id,
        "date": date
    }
    response = requests.post(f"{PAYMENTS_SERVICE_URL}/payments", json=payload)
    data = response.json()

    if response.status_code == 201:
        return {
            "message": data["message"],
            "error": None,
            "status": data["status"]
        }
    else:
        return {
            "message": "Error adding payment",
            "error": data["error"],
            "status": data["status"]
        }
