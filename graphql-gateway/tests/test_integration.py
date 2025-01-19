from unittest.mock import patch
import pytest
from starlette.testclient import TestClient
from src.main import app  # Replace with the actual app import

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_list_users_with_mock(client):
    # Define the GraphQL query
    query = """
    query {
        listUsers {
            id
            username
            email
            dob
        }
    }
    """

    # Mock data that the resolver should return
    mock_users = [
        {"id": "1", "username": "testuser1", "email": "test1@example.com", "dob": "2000-01-01"},
        {"id": "2", "username": "testuser2", "email": "test2@example.com", "dob": "1995-05-05"},
    ]

    # Patch the database call or resolver method
    with patch("myapp.resolvers.user_resolvers.resolve_list_users") as mock_resolver:
        mock_resolver.return_value = mock_users

        # Send the query using the test client
        response = client.post("/graphql", json={"query": query})

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "listUsers" in data["data"]
        users = data["data"]["listUsers"]
        assert users == mock_users