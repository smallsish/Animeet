import json
import pytest


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


@pytest.mark.dependency()
def test_health(client):
    result = call(client, 'health')
    assert result['code'] == 200


@pytest.mark.dependency()
def test_get_all(client):
    result = call(client, 'events')
    assert result['code'] == 200
    assert result['json']['data']['events'] == [
      {
        "capacity": 50,
        "slots_left": 50,
        "description": "An evening of classical music with a live orchestra.",
        "entry_fee": 50.0,
        "event_id": 1,
        "event_name": "Music Concert",
        "time": "Wed, 25 Dec 2024 19:00:00 GMT",
        "venue": "City Hall"
      }
    ]


# This is not a dependency per se (the tests can be
# executed in any order). But if 'test_get_all' does
# not pass, there's no point in running any other
# test, so may as well skip them.

@pytest.mark.dependency(depends=['test_get_all'])
def test_one_valid(client):
    result = call(client, 'events/1')
    assert result['code'] == 200
    assert result['json']['data'] == {
        "capacity": 50,
        "slots_left": 50,
        "description": "An evening of classical music with a live orchestra.",
        "entry_fee": 50.0,
        "event_id": 1,
        "event_name": "Music Concert",
        "time": "Wed, 25 Dec 2024 19:00:00 GMT",
        "venue": "City Hall"
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_one_invalid(client):
    result = call(client, 'events/2')
    assert result['code'] == 404
    assert result['json'] == {
        "message": "Event not found."
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_update_existing_event(client):
    result = call(client, 'events/1', 'PATCH', {
        "capacity": 40,
        "slots_left": 40,
        "event_name": "Music Concert: The Special"
    })
    assert result['code'] == 200
    assert result['json']['data'] == {
        "capacity": 40,
        "slots_left": 40,
        "description": "An evening of classical music with a live orchestra.",
        "entry_fee": 50.0,
        "event_id": 1,
        "event_name": "Music Concert: The Special",
        "time": "Wed, 25 Dec 2024 19:00:00 GMT",
        "venue": "City Hall"
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_create_no_body(client):
    result = call(client, 'events', 'POST', {})
    assert result['code'] == 500


@pytest.mark.dependency(depends=['test_get_all', 'test_create_no_body'])
def test_create_one_event(client):
    result = call(client, 'events', 'POST', {
        "event_name": "Art Exhibition",
        "venue": "Art Gallery",
        "entry_fee": 20,
        "time": "2024-12-30 10:00:00",
        "description": "A showcase of modern art.",
        "slots_left": 70,
        "capacity": 70
    })
    assert result['code'] == 201
    assert result['json']['data'] == {
        "event_id": 2,
        "event_name": "Art Exhibition",
        "venue": "Art Gallery",
        "entry_fee": 20,
        "time": "Mon, 30 Dec 2024 10:00:00 GMT",
        "description": "A showcase of modern art.",
        "slots_left": 70,
        "capacity": 70
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_delete_event(client):
    result = call(client, 'events/1', 'DELETE')
    assert result['code'] == 200
    assert result['json']['data'] == {
        "event_id": 1
    }


@pytest.mark.dependency(depends=['test_delete_event'])
def test_deleted_event(client):
    call(client, 'events/1', 'DELETE')
    result = call(client, 'events/1', 'GET')
    assert result['code'] == 404
    assert result['json'] == {
        "message": "Event not found."
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_reserve_event(client):
    result = call(client, 'events/1', 'PATCH', {
        "reserve": 5
    })
    assert result['code'] == 200
    assert result['json']['data'] == {
        "capacity": 50,
        "slots_left": 45,
        "description": "An evening of classical music with a live orchestra.",
        "entry_fee": 50.0,
        "event_id": 1,
        "event_name": "Music Concert",
        "time": "Wed, 25 Dec 2024 19:00:00 GMT",
        "venue": "City Hall"
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_reserve_event_all(client):
    result = call(client, 'events/1', 'PATCH', {
        "reserve": 50
    })
    assert result['code'] == 200
    assert result['json']['data'] == {
        "capacity": 50,
        "slots_left": 0,
        "description": "An evening of classical music with a live orchestra.",
        "entry_fee": 50.0,
        "event_id": 1,
        "event_name": "Music Concert",
        "time": "Wed, 25 Dec 2024 19:00:00 GMT",
        "venue": "City Hall"
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_unreserve_event(client):
    result = call(client, 'events/1', 'PATCH', {
        "reserve": 5
    })
    result = call(client, 'events/1', 'PATCH', {
        "reserve": -4
    })
    assert result['code'] == 200
    assert result['json']['data'] == {
        "capacity": 50,
        "slots_left": 49,
        "description": "An evening of classical music with a live orchestra.",
        "entry_fee": 50.0,
        "event_id": 1,
        "event_name": "Music Concert",
        "time": "Wed, 25 Dec 2024 19:00:00 GMT",
        "venue": "City Hall"
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_reserve_existing_event_fail(client):
    result = call(client, 'events/1', 'PATCH', {
        "reserve": 51
    })
    assert result['code'] == 500


@pytest.mark.dependency(depends=['test_get_all'])
def test_reserve_nonexisting_event(client):
    result = call(client, 'events/555', 'PATCH', {
        "reserve": 16
    })
    assert result['code'] == 404