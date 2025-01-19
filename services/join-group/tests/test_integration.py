import json
import pytest
from unittest.mock import patch, call, MagicMock

GROUPS_SERVICE_URL = 'http://groups:5000'
USERS_SERVICE_URL = 'http://users:5000'

def client_call(client, path, method='GET', body=None):
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


@pytest.mark.dependency()
def test_health(client):
    result = client_call(client, 'health')
    assert result['code'] == 200


@patch('src.app.requests.post')
@patch('src.app.requests.get')
def test_join_group_pass(mock_get, mock_post, client):
    # Mock the response for the first POST request (join group)
    mock_post_response = MagicMock()
    mock_post_response.status_code = 201
    mock_post_response.json.return_value = {
        "data": {
            "joined": "Wed, 22 Sep 2021 14:51:05 GMT",
            "group_id": 1,
            "user_id": 1,
            "role": 'Leader',
            "status": "NEW",
            "members": [1]
        },
        "message": "Successfully joined the group."
    }
    
    # Mock a second POST request for notifying group members
    mock_notification_response = MagicMock()
    mock_notification_response.status_code = 200
    mock_notification_response.json.return_value = {
        "message": "Notification request sent to queue",
        "subject": "Group join success",
        "body": "You have joined a group!",
        "email": 'johndoe@example.com'
    }
    
    # Configure the mock to return the notification response on the second call
    mock_post.side_effect = [mock_post_response, mock_notification_response]

    # Mock the response for the GET request
    mock_get_event_response = MagicMock()
    mock_get_event_response.status_code = 200
    mock_get_event_response.json.return_value = {
        "data": {
            "capacity": 50,
            "slots_left": 50,
            "description": "An evening of classical music with a live orchestra.",
            "entry_fee": 50.0,
            "event_id": 1,
            "event_name": "Music Concert",
            "time": "Wed, 25 Dec 2024 19:00:00 GMT",
            "venue": "City Hall"
        }
    }
    
    # Mock the response for the GET request
    mock_get_user_response = MagicMock()
    mock_get_user_response.status_code = 200
    mock_get_user_response.json.return_value = {
        "user": {
            "id": 1,
            "username": "johndoe"
        },
        'email': 'johndoe@example.com',
        'dob': '1990-05-15',
    }
    mock_get.side_effect = [mock_get_user_response, mock_get_event_response]

    # Use the client_call() function to make the POST request to /join-group
    result = client_call(client, '/join-group/1', method='POST', body={
        "user_id": 1,
        "event_id": 1
    })

    # Check that the response status code and data match expectations
    assert result['code'] == 201
    assert result['json']['data']['members'] == [1]

    mock_post.assert_any_call("http://groups:5000/groups/1",
        data=json.dumps({
            "user_id": 1
        }),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    assert mock_get.call_count == 2  # Expecting two calls to GET
    mock_get.assert_has_calls([
        call("http://users:5000/users/1"),
        call("http://events:5000/events/1"),
    ], any_order=True)

    assert mock_post.call_count == 2  # Expecting two calls to POST

    # Check the parameters for the second POST call
    assert mock_post.call_args_list[1] == call('http://notifications:5000/publish-join-notification', data='{"email": "johndoe@example.com", "subject": "Group join success", "body": "You have joined a group!"}', headers={'Content-Type': 'application/json', 'Accept': 'application/json'})


@patch('src.app.requests.post')
@patch('src.app.requests.get')
def test_join_group_fail(mock_get, mock_post, client):
    # Mock the response for the POST request
    mock_post_response = MagicMock()
    mock_post_response.status_code = 500
    mock_post_response.json.return_value = {
        "message": "Unable to join group.",
        "error": "Group is full."
    }
    mock_post.return_value = mock_post_response

    # Mock the response for the GET request
    mock_get_user_response = MagicMock()
    mock_get_user_response.status_code = 200
    mock_get_user_response.json.return_value = {
        "user": {
            "id": 1,
            "username": "johndoe"
        },
        'email': 'johndoe@example.com',
        'dob': '1990-05-15',
    }

    # Mock the response for the GET request
    mock_get_event_response = MagicMock()
    mock_get_event_response.status_code = 200
    mock_get_event_response.json.return_value = {
        "data": {
            "capacity": 50,
            "slots_left": 50,
            "description": "An evening of classical music with a live orchestra.",
            "entry_fee": 50.0,
            "event_id": 1,
            "event_name": "Music Concert",
            "time": "Wed, 25 Dec 2024 19:00:00 GMT",
            "venue": "City Hall"
        }
    }

    mock_get.side_effect = [mock_get_user_response, mock_get_event_response]

    # Use the call() function to make the POST request to /join-group
    result = client_call(client, '/join-group/1', method='POST', body={
        "user_id": 1,
        "event_id": 1
    })

    # Check that the response status code and data match expectations
    assert result['code'] == 500
    assert result['json'] == {
        "message": "Unable to join group.",
        "error": "Group is full."
    }

    mock_post.assert_called_once_with("http://groups:5000/groups/1",
        data=json.dumps({
            "user_id": 1
        }),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })


@patch('src.app.requests.post')
@patch('src.app.requests.get')
def test_join_group_event_fail(mock_get, mock_post, client):
    # Mock the response for the GET request
    mock_get_user_response = MagicMock()
    mock_get_user_response.status_code = 200
    mock_get_user_response.json.return_value = {
        "user": {
            "id": 1,
            "username": "johndoe"
        },
        'email': 'johndoe@example.com',
        'dob': '1990-05-15',
    }

    # Mock the response for the GET request
    mock_get_event_response = MagicMock()
    mock_get_event_response.status_code = 200
    mock_get_event_response.json.return_value = {
        "data": {
            "capacity": 50,
            "slots_left": 0,
            "description": "An evening of classical music with a live orchestra.",
            "entry_fee": 50.0,
            "event_id": 1,
            "event_name": "Music Concert",
            "time": "Wed, 25 Dec 2024 19:00:00 GMT",
            "venue": "City Hall"
        }
    }
    mock_get.side_effect = [mock_get_user_response, mock_get_event_response]

    # Use the call() function to make the POST request to /join-group
    result = client_call(client, '/join-group/1', method='POST', body={
        "user_id": 1,
        "event_id": 1
    })

    # Check that the response status code and data match expectations
    assert result['code'] == 400
    assert result['json'] == {
        "message": "Unable to join group, event is out of slots."
    }

    mock_get.assert_has_calls([
        call("http://users:5000/users/1"),
        call("http://events:5000/events/1")
    ], any_order=True)


@patch('src.app.requests.post')
@patch('src.app.requests.get')
def test_join_group_with_members(mock_get, mock_post, client):
    # Mock the response for the POST request
    mock_post_response = MagicMock()
    mock_post_response.status_code = 201
    mock_post_response.json.return_value = {
        "data": {
            "joined": "Wed, 22 Sep 2021 14:51:05 GMT",
            "group_id": 1,
            "user_id": 3,
            "role": 'Leader',
            "status": "NEW",
            "members": [1, 2, 3]
        },
        "message": "Successfully joined the group."
    }

    # Mock additional POST requests for notifications
    notification_responses = [
        MagicMock(status_code=200, json=lambda: {"message": f"Notification request sent to queue"}),
        MagicMock(status_code=200, json=lambda: {"message": f"Notification request sent to queue"}),
        MagicMock(status_code=200, json=lambda: {"message": f"Notification request sent to queue"}),
    ]
    
    # Set the side effect for the mock_post to return the notification responses
    mock_post.side_effect = [mock_post_response] + notification_responses
    
    
    mock_get.side_effect = [
        MagicMock(status_code=200, json=lambda: {
            "user": {
                "id": 1,
                "username": "johndoe"
            },
            'email': 'johndoe@example.com',
            'dob': '1990-05-15',
        }),
        MagicMock(status_code=200, json=lambda: {
            "data": {
                "capacity": 50,
                "slots_left": 50,
                "description": "An evening of classical music with a live orchestra.",
                "entry_fee": 50.0,
                "event_id": 1,
                "event_name": "Music Concert",
                "time": "Wed, 25 Dec 2024 19:00:00 GMT",
                "venue": "City Hall"
            }
        }),
        MagicMock(status_code=200, json=lambda: {
            "user": {
                "id": 2,
                "username": "johndoe"
            },
            'email': 'johndoe@example.com',
            'dob': '1990-05-15',
        }),
        MagicMock(status_code=200, json=lambda: {
            "user": {
                "id": 3,
                "username": "johndoe"
            },
            'email': 'johndoe@example.com',
            'dob': '1990-05-15',
        })
    ]

    # Use the client_call() function to make the POST request to /join-group
    result = client_call(client, '/join-group/1', method='POST', body={
        "user_id": 3,
        "event_id": 1
    })

    # Check that the response status code and data match expectations
    assert result['code'] == 201
    assert result['json']['data']['members'] == [1, 2, 3]
    
    mock_get.assert_has_calls([
        call("http://users:5000/users/1"),
        call("http://users:5000/users/2"),
        call("http://users:5000/users/3")
    ], any_order=True)

    # Assert that notifications were sent
    expected_calls = [
        call("http://groups:5000/groups/1",
            data=json.dumps({
                "user_id": 3
            }),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
        }),
        call("http://notifications:5000/publish-join-notification",
            data=json.dumps({
                'email': 'johndoe@example.com',
                "subject": "Update in your event Music Concert",
                "body": "johndoe has joined your group."
            }), 
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'
        }),
        call("http://notifications:5000/publish-join-notification",
            data=json.dumps({
                'email': 'johndoe@example.com',
                "subject": "Update in your event Music Concert",
                "body": "johndoe has joined your group."
            }),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'
        }),
        call("http://notifications:5000/publish-join-notification",
            data=json.dumps({
                'email': 'johndoe@example.com',
                "subject": "Group join success",
                "body": "You have joined a group!"
            }),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'
        })
    ]

    # Check that notifications were sent correctly
    assert mock_post.call_count == 4  # One for joining the group, three for notifications
    mock_post.assert_has_calls(expected_calls, any_order=True)


@patch('src.app.requests.post')
@patch('src.app.requests.get')
@patch('src.app.requests.delete')
def test_leave_group_with_members(mock_delete, mock_get, mock_post, client):
    # Mock the response for the POST request
    mock_delete_response = MagicMock()
    mock_delete_response.status_code = 200
    mock_delete_response.json.return_value = {
        "data": {
            "group_id": 1,
            "user_id": 3,
            "members": [1, 2]
        }
    }
    
    mock_delete.return_value = mock_delete_response


    # Use the client_call() function to make the POST request to /join-group
    result = client_call(client, '/leave-group/1/3', method='DELETE')

    # Check that the response status code and data match expectations
    assert result['code'] == 200
    assert result['json']['data']['members'] == [1, 2]
    
    assert mock_delete.call_count == 1  
    mock_delete.assert_any_call(
        'http://groups:5000/groups/1/users/3',
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })


@patch('src.app.requests.post')
@patch('src.app.requests.get')
@patch('src.app.requests.delete')
def test_leave_group_with_member_fail(mock_delete, mock_get, mock_post, client):
    # Mock the response for the POST request
    mock_delete_response = MagicMock()
    mock_delete_response.status_code = 404
    mock_delete_response.json.return_value = {
        "message": "User not found in the group.",
        "data": {
            "group_id": 1,
            "user_id": 3
        }
    }
    
    mock_delete.return_value = mock_delete_response

    # Use the client_call() function to make the DELETE request to /join-group
    result = client_call(client, '/leave-group/1/3', method='DELETE')

    assert result['code'] == 404
    
    assert mock_get.call_count == 0
    assert mock_post.call_count == 0
    assert mock_delete.call_count == 1  
    mock_delete.assert_any_call(
        'http://groups:5000/groups/1/users/3',
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })