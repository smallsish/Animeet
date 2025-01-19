import pytest
from sqlalchemy import text
from src.app import app as flask_app, db  # Import your Flask app and db

@pytest.fixture(scope='session')
def app():
    """Set up the Flask app with a test database configuration."""
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory database for tests

    with flask_app.app_context():
        db.create_all()  # Create tables for the in-memory database
        # Setup database schema and insert test data
        with db.engine.begin() as connection:
            # Drop the payment table if it exists
            connection.execute(text("DROP TABLE IF EXISTS `payment`;"))

            # Create the payment table
            connection.execute(
                text(
                    """CREATE TABLE `payment` (
                    `payment_id` varchar(64) NOT NULL,
                    `user_id` int NOT NULL,
                    `group_id` int NOT NULL,
                    `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (`payment_id`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
                )
            )

            # Insert test data into the payment table
            connection.execute(
                text(
                    """INSERT INTO `payment` VALUES 
                    ('d73357d8-8a9e-4a4c-8b93-e3b403bd643a', 1, 1, '2024-10-10 14:00:00'),
                    ('c3a57b8e-1d8c-4f21-84c7-b2b7c0f2a2d3', 2, 1, '2024-10-11 14:00:00'),
                    ('f8c7b1f8-4c18-49a9-8b7f-abc62df11a45', 3, 2, '2024-10-12 15:00:00');"""
                )
            )
        yield flask_app  # Provide the app for use in tests

        # Cleanup after tests
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()  # Return the test client