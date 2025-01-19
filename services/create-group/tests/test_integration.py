import json
from unittest.mock import MagicMock, patch
import pytest


def call(client, path, method='GET', body=None):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    if method == 'POST':
        response = client.post(path, data=json.dumps(body), headers=headers)
    elif method == 'PUT':
        response = client.put(path, data=json.dumps(body), headers=headers)
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


@pytest.mark.dependency()
def test_health(client):
    result = call(client, 'health')
    assert result['code'] == 200

@patch('requests.post')
@patch('requests.get')
def test_create_group_success(mock_get, mock_post, client):
    # Mock api responses
    # GROUPS POST
    mock_group_response = MagicMock()
    mock_group_response.status_code = 201
    mock_group_response.json.return_value = {
        "data": {
            "group_id": 1,
            "event_id": "101",
            "user_id": "1001",
            "name": "Test Group",
            "max_capacity": 10,
            "description": "This is a test group."
        }
    }

    # EVENTS GET
    mock_event_response = MagicMock()
    mock_event_response.status_code = 200
    mock_event_response.json.return_value = {"data": {
        "event_name": "Music Concert",
        "venue": "City Hall",
        "entry_fee": 50,
        "time": "2024-12-25 19:00:00",
        "description": "An evening of classical music with a live orchestra.",
        "capacity": 50,
        "slots_left": 50
    }}


    mock_post.return_value = mock_group_response
    mock_get.return_value = mock_event_response

    payload = {
        "event_id": "101",
        "user_id": "1001",
        "name": "Test Group",
        "max_capacity": 10,
        "description": "This is a test group."
    }

    response = call(client, '/create-group', method='POST', body=payload)

    # Status code and response assertions for the success case
    assert response['code'] == 201

    mock_post.assert_called_once_with("http://groups:5000/groups",
    data=json.dumps({
        "event_id": "101",
        "user_id": "1001",
        "name": "Test Group",
        "max_capacity": 10,
        "description": "This is a test group."
    }),
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    mock_get.assert_called_once_with(
    "http://events:5000/events/101"
    )

@patch('requests.post')
@patch('requests.get')
def test_create_group_fail_event(mock_get, mock_post, client):
    # Mock api responses
    mock_group_response = MagicMock()
    mock_group_response.status_code = 201
    mock_group_response.json.return_value = {
        "data": {
            "id": 1,
            "event_id": "101",
            "user_id": "1001",
            "name": "Test Group",
            "max_capacity": 10,
            "description": "This is a test group."
        }
    }

    mock_event_response = MagicMock()
    mock_event_response.status_code = 404
    mock_event_response.json.return_value = {
        'message': 'Event not found.',
        "error": "Invalid event ID."
    }

    mock_post.return_value = mock_group_response
    mock_get.return_value = mock_event_response

    payload = {
        "event_id": "101",
        "user_id": "1001",
        "name": "Test Group",
        "max_capacity": 10,
        "description": "This is a test group."
    }

    response = call(client, '/create-group', method='POST', body=payload)

    # Status code and response assertions for the success case
    assert response['code'] == 500
    
    mock_post.assert_not_called()
    
    mock_get.assert_called_once_with(
    "http://events:5000/events/101"
    )

@patch('requests.post')
@patch('requests.get')
def test_create_group_fail_group(mock_get, mock_post, client):
    # Mock api responses
    mock_group_response = MagicMock()
    mock_group_response.status_code = 500
    mock_group_response.json.return_value = {
        "message": "An error occurred creating the group."
    }

    mock_event_response = MagicMock()
    mock_event_response.status_code = 200
    mock_event_response.json.return_value = {"data": {
        "event_name": "Music Concert",
        "venue": "City Hall",
        "entry_fee": 50,
        "time": "2024-12-25 19:00:00",
        "description": "An evening of classical music with a live orchestra.",
        "capacity": 50,
        "slots_left": 50
    }}

    mock_post.return_value = mock_group_response
    mock_get.return_value = mock_event_response

    payload = {
        "event_id": "101",
        "user_id": "1001",
        "name": "Test Group",
        "max_capacity": 10,
        "description": "This is a test group."
    }

    response = call(client, '/create-group', method='POST', body=payload)

    # Status code and response assertions for the success case
    assert response['code'] == 500

    mock_post.assert_called_once_with("http://groups:5000/groups",
    data=json.dumps({
        "event_id": "101",
        "user_id": "1001",
        "name": "Test Group",
        "max_capacity": 10,
        "description": "This is a test group."
    }),
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    assert mock_get.call_count == 1
