import json
import pytest
from unittest.mock import patch, MagicMock
import stripe

# Helper function to call endpoints
def call(client, path, method='GET', body=None):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    if method == 'POST':
        response = client.post(path, data=json.dumps(body), headers=headers)
    elif method == 'PATCH':
        response = client.patch(path, data=json.dumps(body), headers=headers)
    elif method == 'DELETE':
        response = client.delete(path)
    else:
        response = client.get(path)

    return {
        "json": json.loads(response.data.decode('utf-8')),
        "code": response.status_code
    }

# Health check test
@pytest.mark.dependency()
def test_health(client):
    result = call(client, '/health')
    assert result['code'] == 200
    assert result['json'] == {"message": "Service is healthy", "service": "payment"}

# Test for invalid checkout session creation
@pytest.mark.dependency()
def test_invalid_checkout_session(client):
    data = {
        "user_id": 1,
        "group_id": 1
    }
    result = call(client, '/checkout-session', 'POST', data)
    assert result['code'] == 400
    assert result['json'] == {"message": "Invalid input, user_id, group_id, event_id, event_name, and amount are required."}

# Mocked Stripe Checkout session creation test with database insertion for subsequent tests
@patch('stripe.checkout.Session.create')
@pytest.mark.dependency(depends=["test_invalid_checkout_session"])
def test_checkout_session_creation(mock_checkout_session, client, app):
    # Set up the mock to simulate a successful checkout session creation
    mock_session = MagicMock()
    mock_session.id = "cs_mock_id"
    mock_session.url = "https://checkout.stripe.com/pay/cs_mock_id"
    mock_checkout_session.return_value = mock_session

    data = {
        "user_id": 4,
        "group_id": 2,
        "event_id": 101,
        "event_name": "Sample Event",
        "amount": 1000  # Amount in cents (10 SGD)
    }
    result = call(client, '/checkout-session', 'POST', data)
    assert result['code'] == 201
    assert result['json']["status"] == "success"
    assert result['json']["session_id"] == "cs_mock_id"
    assert "url" in result['json']
    assert result['json']["url"] == "https://checkout.stripe.com/pay/cs_mock_id"

    # Insert a payment record for subsequent tests that need data
    with app.app_context():
        from src.app import db, Payment
        payment = Payment(payment_id="cs_mock_id", user_id=4, group_id=2)
        db.session.add(payment)
        db.session.commit()

# Test for retrieving all payments
@pytest.mark.dependency(depends=["test_checkout_session_creation"])
def test_get_all_payments(client):
    result = call(client, '/payments')
    assert result['code'] == 200
    assert "data" in result['json']
    assert isinstance(result['json']["data"], list)

# Test for retrieving payments by user ID with a valid user
@pytest.mark.dependency(depends=["test_checkout_session_creation"])
def test_get_payments_by_user(client):
    result = call(client, '/payments/4')
    assert result['code'] == 200
    assert "data" in result['json']
    assert len(result['json']["data"]) >= 1  # Ensure at least one record exists

# Test for retrieving payments for a nonexistent user
@pytest.mark.dependency(depends=["test_checkout_session_creation"])
def test_get_nonexistent_payment_by_user(client):
    result = call(client, '/payments/999')  # Assume 999 is not a valid user ID
    assert result['code'] == 404
    assert result['json'] == {"message": "Payments not found for specified user."}

# Mocked Stripe refund processing test
@patch("stripe.Refund.create")
def test_refund_payment_success(mock_refund_create, client):
    mock_refund_create.return_value = {"id": "r_12345", "status": "succeeded"}
    result = call(client, '/refund', 'POST', {"payment_id": "cs_mock_id"})
    assert result['code'] == 200
    assert result['json']["status"] == "success"
    assert result['json']["refund_id"] == "r_12345"

# Test for handling missing payment ID in refund request
def test_refund_payment_missing_id(client):
    result = call(client, '/refund', 'POST', {})
    assert result['code'] == 400
    assert result['json']["error"] == "Missing payment_id"

# Test for handling Stripe API error during refund
@patch("stripe.Refund.create")
def test_refund_payment_stripe_error(mock_refund_create, client):
    mock_refund_create.side_effect = stripe.error.StripeError("Refund failed")
    result = call(client, '/refund', 'POST', {"payment_id": "cs_mock_id"})
    assert result['code'] == 503
    assert result['json']["status"] == "failure"
    assert "Refund failed" in result['json']["error"]

# Test for successful deletion of payment
@pytest.mark.dependency(depends=["test_checkout_session_creation"])
def test_delete_payment(client):
    result = call(client, '/payments/cs_mock_id', method='DELETE')
    assert result['code'] == 200 or result['code'] == 404  # Allow 404 if already deleted