import json
import pytest
from time import sleep
from src.app import publish_notification
from unittest.mock import patch
import threading
from src.consumer import consume_notifications

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
def test_health(client):
    result = call(client, '/health')
    assert result['code'] == 200
    assert result['json'] == {"message": "Service is healthy", "service": "notifications"}

# Test for publishing a notification to RabbitMQ and verifying email sending
@patch('src.consumer.send_email')
def test_publish_and_consume_notification(mock_send_email, client):
    data = {
        "user_id": 999,
        "event_id": 999,
        "user_name": "Test User",
        "event_name": "Sample Event",
        "price": 2000,  # In cents, $20.00
        "email": "testuser@example.com"
    }

    # Step 1: Publish a notification to the queue
    publish_result = call(client, '/publish-notification', 'POST', data)
    assert publish_result['code'] == 200
    assert publish_result['json']["message"] == "Notification request sent to queue"

    # Step 2: Start the consumer in a thread to listen to RabbitMQ
    stop_event = threading.Event()
    consumer_thread = threading.Thread(target=consume_notifications, args=(stop_event,))
    consumer_thread.start()

    # Allow time for the consumer to process the message
    sleep(5)

    # Step 3: Verify that the mock email was sent with expected data
    mock_send_email.assert_called_once_with(
        recipient="testuser@example.com",
        user_name="Test User",
        event_name="Sample Event",
        price=20.00  # Converted from cents
    )

    # Stop the consumer thread
    stop_event.set()
    consumer_thread.join()