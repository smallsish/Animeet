import json
import pytest
from datetime import datetime, timedelta

# TODO after every service has been implemented: 
# - Unable to create group, event registration is over
# - Unable to create group, no tickets left

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


# Get all groups
@pytest.mark.dependency()
def test_get_all(client):
    result = call(client, 'groups')
    assert result['code'] == 200
    assert result['json']['data'] == [
        {
            "description": "Group for cosplay lovers",
            "event_id": 1,
            "group_id": 28, # group_id always starts at 28
            "max_capacity": 5,
            "name": "Cosplay Enthusiasts",
            "slots_left": 3
        },
        {
            "description": "Group for testing lovers",
            "event_id": 2,
            "group_id": 29, 
            "max_capacity": 15,
            "name": "Testing Enthusiasts",
            "slots_left": 14
        }
        
    ]
    

# Get all groups in an event
@pytest.mark.dependency(depends=['test_get_all'])
def test_get_all_with_event_id(client):
    result = call(client, 'groups?event_id=1')
    assert result['code'] == 200
    assert result['json']['data'] == [
        {
            "description": "Group for cosplay lovers",
            "event_id": 1,
            "group_id": 28, 
            "max_capacity": 5,
            "name": "Cosplay Enthusiasts",
            "slots_left": 3
        }
    ]
    
    
# Get all groups from an invalid event id
@pytest.mark.dependency(depends=['test_get_all', 'test_get_all_with_event_id'])
def test_get_all_with_wrong_event_id(client):
    result = call(client, 'groups?event_id=12345')
    assert result['code'] == 404
    assert result['json'] == {
        "message": f"No groups found for event_id 12345."
    }
    
    
# Get one group using valid group id
@pytest.mark.dependency(depends=['test_get_all'])
def test_one_valid(client):
    result = call(client, 'groups/28')
    assert result['code'] == 200
    assert result['json']['data'] == {
        "description": "Group for cosplay lovers",
        "event_id": 1,
        "group_id": 28, # group_id always starts at 28
        "max_capacity": 5,
        "name": "Cosplay Enthusiasts",
        "slots_left": 3
    }


# Get one group using invalid group id
@pytest.mark.dependency(depends=['test_get_all', 'test_one_valid'])
def test_one_invalid(client):
    result = call(client, 'groups/12345')
    assert result['code'] == 404
    assert result['json'] == {
       "message": "Group not found."
    }

# Get all users in a group
@pytest.mark.dependency(depends=['test_get_all'])
def test_get_users_in_one_group(client):
    result = call(client, 'groups/28/users')
    assert result['code'] == 200
    assert result['json']['data'] == [
        {
            "date_joined": 'Sat, 28 Sep 2024 10:32:12 GMT',
            "group_id": 28,
            "role": 'leader', 
            "user_id": 1000,
            "payment_status": 'unpaid'
        }, {
            "date_joined": 'Mon, 30 Sep 2024 11:39:18 GMT',
            "group_id": 28,
            "role": 'member', 
            "user_id": 1001,
            "payment_status": 'unpaid'
        }
    ]
    
    
# Get one user in group-member table
@pytest.mark.dependency(depends=['test_get_all', 'test_get_users_in_one_group'])
def test_get_one_user_in_one_group(client):
    result = call(client, 'groups/28/users/1000')
    assert result['code'] == 200
    assert result['json']['data'] == {
        "date_joined": 'Sat, 28 Sep 2024 10:32:12 GMT',
        "group_id": 28,
        "role": 'leader', 
        "user_id": 1000,
        "payment_status": 'unpaid'
    }
    
    
# Get one user in group-member table with invalid user id
@pytest.mark.dependency(depends=['test_get_all', 'test_get_one_user_in_one_group'])
def test_cannot_find_user_in_one_group(client):
    result = call(client, 'groups/28/users/12345678')
    assert result['code'] == 404
    assert result['json']['message'] == "User not found."
    
    
# Create group without giving any body
@pytest.mark.dependency(depends=['test_get_all'])
def test_create_no_body(client):
    result = call(client, 'groups', 'POST', {})
    assert result['code'] == 500
    
    
# User creates a group
@pytest.mark.dependency(depends=['test_get_all', 'test_create_no_body'])
def test_create_one_group(client):
    result = call(client, 'groups', 'POST', {
                    "event_id": 2,
                    "user_id": 1001,
                    "name": "Anime Group",
                    "max_capacity": 10,
                    "description": "A group for people who loves anime."
                })
    assert result['code'] == 201
    assert result['json']['message'] == "Group has been created successfully."
    assert result['json']['data'] == {
        "description": "A group for people who loves anime.",
        "event_id": 2,
        "group_id": 30,
        "max_capacity": 10,
        "name": "Anime Group",
        "slots_left": 9
    }
   
   
# User joins a group
@pytest.mark.dependency(depends=['test_get_all', 'test_create_no_body', 'test_one_valid'])
def test_join_one_group(client):
    
    current_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    # Add 1 second to the current date
    current_date_plus_one = (datetime.now() + timedelta(seconds=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    current_date_minus_one = (datetime.now() - timedelta(seconds=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    possible_dates = [current_date, current_date_plus_one,  current_date_minus_one]
    
    result = call(client, 'groups/28', 'POST', {
        "user_id": 1003
    })
    
    assert result['code'] == 201
    assert result['json']['message'] == 'Successfully joined the group.'
    assert result['json']['data'] == {
            "joined": possible_dates[0],
            "group_id": 28,
            "user_id": 1003,
            "role": 'member',
            "status": 'NEW',
            "members": [1000, 1001, 1003]
        } or {
            "joined": possible_dates[1],
            "group_id": 28,
            "user_id": 1003,
            "role": 'member',
            "status": 'NEW',
            "members": [1000, 1001, 1003]
        } or {
            "joined": possible_dates[2],
            "group_id": 28,
            "user_id": 1003,
            "role": 'member',
            "status": 'NEW',
            "members": [1000, 1001, 1003]
        }
       
    
# Check if the remaining slot has been reduced by 1 after new user joins
@pytest.mark.dependency(depends=['test_get_all', 'test_join_one_group'])
def test_slots_left_deducted_after_join(client):
    
    call(client, 'groups/28', 'POST', {
        "user_id": 1003
    })
    result = call(client, 'groups/28')
    assert result['code'] == 200
    assert result['json']['data'] == {
        "description": "Group for cosplay lovers",
        "event_id": 1,
        "group_id": 28,
        "max_capacity": 5,
        "name": "Cosplay Enthusiasts",
        "slots_left": 2
    }


# Delete a user from a group
@pytest.mark.dependency(depends=['test_get_all', 'test_join_one_group', 'test_slots_left_deducted_after_join'])
def test_delete_user_from_group(client):
    call(client, 'groups/28', 'POST', {
        "user_id": 1003
    })
    result = call(client, '/groups/28/users/1003', 'DELETE')
    assert result['code'] == 200
    assert result['json']['data'] == {
        "group_id": 28,
        "members": [1000, 1001],
        "user_id": 1003
    }
    


# Check if user was really deleted from group
@pytest.mark.dependency(depends=['test_get_all', 'test_join_one_group', 'test_delete_user_from_group'])
def test_deleted_user_from_group(client):
    call(client, 'groups/28', 'POST', {
        "user_id": 1003
    })
    call(client, '/groups/28/users/1003', 'DELETE')
    result = call(client, '/groups/28/users', 'GET')
    assert result['code'] == 200
    assert result['json']['data'] == [
        {
            "date_joined": 'Sat, 28 Sep 2024 10:32:12 GMT',
            "group_id": 28,
            "role": 'leader', 
            "user_id": 1000,
            "payment_status": 'unpaid'
        }, {
            "date_joined": 'Mon, 30 Sep 2024 11:39:18 GMT',
            "group_id": 28,
            "role": 'member', 
            "user_id": 1001,
            "payment_status": 'unpaid'
        }
    ]

# Check if slots remaining is added by 1 after user leaves a group
@pytest.mark.dependency(depends=['test_get_all', 'test_join_one_group', 'test_delete_user_from_group', 'test_one_valid'])
def test_add_1_slots_remaining_after_user_leaves(client):
    call(client, 'groups/28', 'POST', {
        "user_id": 1003
    })
    call(client, '/groups/28/users/1003', 'DELETE')
    result = call(client, '/groups/28', 'GET')
    assert result['code'] == 200
    assert result['json']['data'] == {
        "description": "Group for cosplay lovers",
        "event_id": 1,
        "group_id": 28, 
        "max_capacity": 5,
        "name": "Cosplay Enthusiasts",
        "slots_left": 3
    }
    


# Delete a group with valid id
@pytest.mark.dependency(depends=['test_get_all'])
def test_delete_group_valid_id(client):
    result = call(client, 'groups/29', 'DELETE')
    assert result['code'] == 200
    assert result['json']['data'] == {
        "group_id": 29
    }


# Delete a group with invalid id 
@pytest.mark.dependency(depends=['test_get_all'])
def test_delete_group_invalid_id(client):
    result = call(client, 'groups/12345', 'DELETE')
    assert result['code'] == 404
    assert result['json'] == {
        "message": "Group not found.",
        "data" : {'group_id': 12345}
    }
    assert result['json']['data'] == {
        "group_id": 12345
    }


# Check that a group has really been deleted
@pytest.mark.dependency(depends=['test_delete_group_valid_id'])
def test_deleted_group(client):
    call(client, 'groups/29', 'DELETE')
    result = call(client, 'groups/29', 'GET')
    assert result['code'] == 404
    assert result['json'] == {
        "message": "Group not found."
    }
    
# Check if user payment status is successfully changed
@pytest.mark.dependency(depends=['test_get_all'])
def test_change_user_payment_status(client):
    result = call(client, 'groups/28/users/1000', 'PATCH', {
        "payment_status": 'paid'
    })
    assert result['code'] == 200
    assert result['json']['data'] == {
        "group_id": 28,
        "user_id": 1000,
        "payment_status": 'paid',
        "role": 'leader'
    }
    
    
# Check if user role is successfully changed
@pytest.mark.dependency(depends=['test_get_all'])
def test_change_user_role(client):
    result = call(client, 'groups/28/users/1001', 'PATCH', {
        "role": 'leader'
    })
    assert result['code'] == 200
    assert result['json']['data'] == {
        "group_id": 28,
        "user_id": 1001,
        "payment_status": 'unpaid',
        "role": 'leader'
    }
