"""
Contains all tests for the HTTPS API endpoint for users.
"""

# Standard Library Imports
from unittest import IsolatedAsyncioTestCase
from uuid import uuid4

# Third Party Imports
from fastapi.testclient import TestClient
from httpx import Response

# Local Imports
from api.api import app

# Constants


class TestUsers(IsolatedAsyncioTestCase):
    """
    Test the HTTPS API endpoint for users.
    """

    def test_post_users_bad_password(self):
        """
        Test the POST method for the users endpoint with an insecure password.
        """
        # Create a test client
        client: TestClient = TestClient(app)

        # Create a user id for the testing
        user_id: str = str(uuid4())

        # Make the request
        response: Response = client.post("/users", data={"username": f"test-{user_id}", "email": f"test-{user_id}@testing.blackhole", "password": "password"})
        assert response.status_code == 430

        print(response)

        assert response.json() == {"message": "POST users"}
