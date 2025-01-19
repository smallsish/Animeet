import pytest
import json
from src.app import app
from unittest.mock import patch
import requests

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"message": "Service is healthy", "service": "Make a Payment"}

def test_make_payment_success(client):
    """Test make-a-payment process success flow using WireMock mappings."""
    user_id = "user123"
    group_id = "group123"
    event_id = "event123"

    # Setup WireMock mappings for mock responses
    wiremock_url = "http://wiremock:8080"

    # Mock response for reserving an event slot
    requests.post(f"{wiremock_url}/__admin/mappings", json={
        "request": {
            "method": "PATCH",
            "url": f"/events/{event_id}"
        },
        "response": {
            "status": 200,
            "jsonBody": {"message": "Slot reserved successfully"},
        }
    })

    # Mock response for retrieving event details
    requests.post(f"{wiremock_url}/__admin/mappings", json={
        "request": {
            "method": "GET",
            "url": f"/events/{event_id}"
        },
        "response": {
            "status": 200,
            "jsonBody": {
                "data": {
                    "entry_fee": 100,
                    "event_name": "Sample Event",
                    "time": "Wed, 25 Dec 2024 19:00:00 GMT"
                }
            },
        }
    })

    # Mock response for creating a payment session
    requests.post(f"{wiremock_url}/__admin/mappings", json={
        "request": {
            "method": "POST",
            "url": "/checkout-session"
        },
        "response": {
            "status": 201,
            "jsonBody": {
                "url": "http://stripe-session-url"
            }
        }
    })

    # Request payload
    payload = {
        "user_id": user_id,
        "group_id": group_id,
        "event_id": event_id
    }

    # Test the make-a-payment endpoint
    response = client.post("/make-a-payment", json=payload)
    assert response.status_code == 201
    assert response.json["status"] == "success"
    assert "url" in response.json
    assert response.json["url"] == "http://stripe-session-url"

@patch("stripe.Webhook.construct_event")
def test_stripe_webhook_success(mock_construct_event, client):
    """Test the stripe_webhook endpoint on successful payment completion."""
    
    # Setup WireMock mappings for mock responses
    wiremock_url = "http://wiremock:8080"

    # Mock response for updating payment status
    requests.post(f"{wiremock_url}/__admin/mappings", json={
        "request": {
            "method": "PATCH",
            "url": f"/groups/group123/users/user123"
        },
        "response": {
            "status": 200,
            "jsonBody": {"message": "Payment status updated successfully"},
        }
    })

    # Mock response for retrieving user details
    requests.post(f"{wiremock_url}/__admin/mappings", json={
        "request": {
            "method": "GET",
            "url": f"/users/user123"
        },
        "response": {
            "status": 200,
            "jsonBody": {
                "user": {
                    "username": "Test User",
                    "email": "testuser@example.com"
                }
            }
        }
    })

    # Mock response for logging payment in Payment service
    requests.post(f"{wiremock_url}/__admin/mappings", json={
        "request": {
            "method": "POST",
            "url": "/payments"
        },
        "response": {
            "status": 201,
            "jsonBody": {
                "message": "Payment logged successfully"
            }
        }
    })

    # Mock construct_event to bypass signature verification
    payload = {
        "id": "evt_test_webhook",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "payment_intent": "pi_test_intent",
                "metadata": {
                    "user_id": "user123",
                    "group_id": "group123",
                    "event_id": "event123",
                    "event_name": "Sample Event",
                    "price": "100.0"
                }
            }
        }
    }
    mock_construct_event.return_value = payload

    # Provide a Stripe-Signature header (no real verification needed here)
    headers = {"Stripe-Signature": "t=123456789,v1=fake_signature"}

    # Test the webhook endpoint
    response = client.post("/webhook", data=json.dumps(payload), headers=headers)

    # Assertions to verify the response and the flow
    assert response.status_code == 200
    assert response.json["status"] == "success"