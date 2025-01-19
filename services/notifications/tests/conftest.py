import pytest
from src.app import app

@pytest.fixture(scope="session")
def client():
    # Configure app for testing
    app.config["TESTING"] = True

    # Initialize test client
    with app.test_client() as client:
        yield client