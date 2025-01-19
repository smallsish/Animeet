import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
import logging
import stripe
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variable configurations for service URLs
# EVENTS_SERVICE_URL = os.getenv("EVENTS_SERVICE_URL", "http://localhost:5000")
# PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "http://localhost:5001")
# GROUPS_SERVICE_URL = os.getenv("GROUPS_SERVICE_URL", "http://localhost:5002")
# USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://localhost:5003")
# NOTIFICATIONS_SERVICE_URL = os.getenv("NOTIFICATIONS_SERVICE_URL", "http://localhost:5004")  # noqa: E501


EVENTS_SERVICE_URL = os.getenv("events_service_url_internal", "http://wiremock:8080")
PAYMENT_SERVICE_URL = os.getenv("payment_service_url_internal", "http://wiremock:8080")
GROUPS_SERVICE_URL = os.getenv("groups_service_url_internal", "http://wiremock:8080")
USERS_SERVICE_URL = os.getenv("users_service_url_internal", "http://wiremock:8080")
NOTIFICATIONS_SERVICE_URL = os.getenv("notifications_service_url_internal", "http://wiremock:8080")  # noqa: E501
MAKE_A_PAYMENT_SERVICE_URL = os.getenv("make_a_payment_service_url_internal", "http://wiremock:8080")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# EVENTS_SERVICE_URL=http://wiremock:8080
# PAYMENT_SERVICE_URL=http://wiremock:8080
# GROUPS_SERVICE_URL=http://wiremock:8080
# USERS_SERVICE_URL=http://wiremock:8080
# NOTIFICATIONS_SERVICE_URL=http://wiremock:8080
# WIREMOCK_URL=http://wiremock:8080

# EVENTS_SERVICE_URL = "http://events:5000"
# PAYMENT_SERVICE_URL = "http://payments:5000"
# GROUPS_SERVICE_URL = "http://groups:5000"
# USERS_SERVICE_URL = "http://users:5000"
# NOTIFICATIONS_SERVICE_URL = "http://notifications:5000"
# # MAKE_A_PAYMENT_SERVICE_URL = os.getenv("MAKE-A-PAYMENT_URL", "http://localhost:5000")
# STRIPE_WEBHOOK_SECRET = "whsec_34fe1fb383f13e0150bfd7e1b84e77a939722cf30d06fa032d5ff30f931511a1"

@app.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint to confirm the service is up."""
    return jsonify({
        "message": "Service is healthy",
        "service": "Make a Payment"
    }), 200


def get_event_details(event_id):
    """
    Retrieve event details (price and name) using the Events service.
    """
    response = requests.get(f"{EVENTS_SERVICE_URL}/events/{event_id}")
    if response.status_code == 200:
        event_data = response.json().get("data", {})

        # Check if all required keys are present
        if not all(key in event_data for key in ["entry_fee", "event_name", "time"]):
            logger.error(f"Missing keys in event data: {event_data}")
            return None, None, None

        return event_data["entry_fee"], event_data["event_name"], event_data["time"]
    else:
        logger.error(f"Failed to retrieve event details: {response.status_code}, {response.text}")
        return None, None, None


def get_user_details(user_id):
    """
    Retrieve user information (name and email) using the Users service.
    """
    try:
        response = requests.get(f"{USERS_SERVICE_URL}/users/{user_id}")
        response_data = response.json()
        logger.info(f"Users service response: {response_data}")
        
        if response.status_code == 200 and "user" in response_data:
            user_data = response_data["user"]
            email = response_data.get("email")
            user_name = user_data.get("username")
            if user_name and email:
                return user_name, email
            else:
                logger.error("Username or email missing in the response.")
                return None, None
        else:
            logger.error("Failed to retrieve user details or unexpected response format.")
            return None, None
    except Exception as e:
        logger.error(f"Error retrieving user details: {e}")
        return None, None


def reserve_event_slot(event_id):
    """
    Reserve a single slot for an event.
    """
    payload = {"reserve": 1}  # Reserve one slot
    response = requests.patch(
        f"{EVENTS_SERVICE_URL}/events/{event_id}",
        json=payload
    )
    return response


def release_event_slot(event_id):
    """
    Release a single reserved slot for an event.
    """
    payload = {"reserve": -1}  # Release one slot
    response = requests.patch(
        f"{EVENTS_SERVICE_URL}/events/{event_id}",
        json=payload
    )
    return response


def post_payment(user_id, group_id, event_id, event_name, price, amount):
    """
    Make a payment request to the Payment service.
    """
    payload = {
        "user_id": user_id,
        "group_id": group_id,
        "event_id": event_id,      # Add event_id to the payload
        "event_name": event_name,  # Add event_name to the payload
        "price": price,            # Add price to the payload
        "amount": amount           # Amount in smallest currency unit (e.g., cents)
    }
    response = requests.post(
        f"{PAYMENT_SERVICE_URL}/checkout-session",
        json=payload
    )
    return response


def update_payment_status(group_id, user_id, status="paid"):
    """
    Update the payment status of a user within a group using
    the Groups service.
    """
    payload = {
        "payment_status": status
    }
    response = requests.patch(
        f"{GROUPS_SERVICE_URL}/groups/{group_id}/users/{user_id}",
        json=payload
    )
    return response


def publish_notification(user_id, event_id, user_name, event_name, price, email):  # noqa: E501
    """
    Send a notification request to the Notifications service with
    necessary details.
    """
    payload = {
        "user_id": user_id,
        "event_id": event_id,
        "user_name": user_name,
        "event_name": event_name,
        "price": float(price),  # In smallest currency unit, such as cents
        "email": email
    }
    response = requests.post(
        f"{NOTIFICATIONS_SERVICE_URL}/publish-notification",
        json=payload
    )
    return response

@app.route("/make-a-payment", methods=["POST"])
def make_payment():
    """
    Endpoint to initiate the payment process and return the checkout session URL for Stripe payment.
    """
    try:
        # Retrieve data from the request
        data = request.get_json()
        user_id = data.get("user_id")
        group_id = data.get("group_id")
        event_id = data.get("event_id")

        logger.info(f"Starting payment process for user_id: {user_id}, group_id: {group_id}, event_id: {event_id}")

        # Step 1: Reserve an event slot
        reserve_response = reserve_event_slot(event_id)
        if reserve_response.status_code != 200:
            logger.error(f"Event slot reservation failed with response: {reserve_response.json()}")
            return jsonify({
                "message": "Event slot reservation failed.",
                "error": reserve_response.json()
            }), 400
        logger.info(f"Reserved slot for event_id: {event_id}")

        # Step 1.5: Check if user has already paid for this event using the payment-status endpoint
        payment_status_response = requests.get(f"{GROUPS_SERVICE_URL}/groups/{group_id}/users/{user_id}/payment-status")
        if payment_status_response.status_code != 200:
            logger.error(f"Failed to retrieve payment status for user_id: {user_id}, group_id: {group_id}.")
            release_event_slot(event_id)
            return jsonify({
                "message": "Failed to retrieve payment status."
            }), 500

        payment_status_data = payment_status_response.json()
        payment_status = payment_status_data.get("payment_status")
        if payment_status == "paid":
            logger.warning(f"User {user_id} has already paid for group_id: {group_id}. Rolling back reservation.")
            release_event_slot(event_id)
            return jsonify({
                "message": "User has already paid for this event."
            }), 400

        # Step 2: Retrieve the event details
        price, event_name, deadline = get_event_details(event_id)
        if price is None or event_name is None:
            logger.error("Failed to retrieve event details or event not found.")
            release_event_slot(event_id)
            return jsonify({
                "message": "Event not found or failed to retrieve details."
            }), 404
        logger.info(f"Retrieved event details - Name: {event_name}, Price: {price}, Deadline: {deadline}")

        # Check if the event deadline has passed
        deadline = datetime.strptime(deadline, "%a, %d %b %Y %H:%M:%S %Z")
        current_time = datetime.now()
        if current_time > deadline:
            logger.warning(f"Event deadline has passed for event_id: {event_id}")
            release_event_slot(event_id)
            return jsonify({
                "message": "Event deadline has passed."
            }), 400

        # Step 3: Create a Stripe checkout session and return the URL
        payment_response = post_payment(user_id, group_id, event_id, event_name, price, int(price * 100))  # Convert to cents
        if payment_response.status_code != 201:
            logger.error(f"Failed to initiate payment session. Response: {payment_response.json()}")
            release_event_slot(event_id)
            return jsonify({
                "message": "Failed to initiate payment session.",
                "error": payment_response.json()
            }), payment_response.status_code

        # Extract the URL for redirection
        session_data = payment_response.json()
        session_url = session_data.get("url")
        if not session_url:
            logger.error("Failed to retrieve session URL from payment service.")
            release_event_slot(event_id)
            return jsonify({
                "message": "Failed to retrieve session URL from payment service."
            }), 500

        logger.info(f"Payment session created successfully for user_id: {user_id}. Session URL: {session_url}")

        # Pass event_name and price along with other data to `post-payment-processing`
        return jsonify({
            "status": "success",
            "url": session_url,
            "event_name": event_name,
            "price": price
        }), 201

    except Exception as e:
        logger.exception("An unexpected error occurred during the payment process.")
        release_event_slot(event_id)
        return jsonify({
            "message": "An error occurred during the payment process.",
            "error": str(e)
        }), 500
    
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    """
    Webhook endpoint to listen for Stripe events.
    """
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    if sig_header is None or not payload:
        logger.error("Missing Stripe signature header or empty payload.")
        return jsonify({"status": "failure", "error": "Invalid request"}), 400

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            payment_intent_id = session["payment_intent"]
            user_id = session["metadata"]["user_id"]
            group_id = session["metadata"]["group_id"]
            event_id = session["metadata"]["event_id"]
            event_name = session["metadata"].get("event_name")
            price = session["metadata"].get("price")

            # Step 1: Update payment status in the Groups service
            update_payment_status(group_id, user_id, "paid")

            # Step 2: Retrieve user details and send a notification
            user_name, user_email = get_user_details(user_id)
            if user_name and user_email:
                publish_notification(user_id, event_id, user_name, event_name, float(price) * 100, user_email)

            # Step 3: Add the successful payment to the Payment service
            payment_payload = {
                "payment_id": payment_intent_id,
                "user_id": user_id,
                "group_id": group_id,
                "date": datetime.now(timezone.utc).isoformat()
            }
            response = requests.post(f"{PAYMENT_SERVICE_URL}/payments", json=payment_payload)
            if response.status_code != 201:
                logger.error(f"Failed to log payment in the Payment service: {response.json()}")
                return jsonify({"status": "failure", "error": "Failed to log payment"}), 500

            return jsonify({"status": "success"}), 200

        elif event["type"] == "checkout.session.expired":
            logger.error(f"Payment session expired for session: {session}")
            return jsonify({"status": "failure", "error": "Payment session expired"}), 400

        return jsonify({"status": "success"}), 200

    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Webhook signature verification failed: {e}")
        return jsonify({"status": "failure", "error": "Invalid signature"}), 400
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return jsonify({"status": "failure", "error": "Webhook processing error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
