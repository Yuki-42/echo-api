"""
Contains all tests for the HTTPS API endpoint for users.
"""

# Standard Library Imports
from unittest import TestCase
from httpx import Response

# Third Party Imports
from fastapi.testclient import TestClient

# Local Imports
from api.api import app


# Constants


class TestUsers(TestCase):
    """
    Test the HTTPS API endpoint for users.
    """

    def test_post_users(self):
        """
        Test the POST method for the users endpoint.
        """
        # Create a test client
        client: TestClient = TestClient(app)

        # Make the request
        response: Response = client.post("/users")
        assert response.status_code == 200
        assert response.json() == {"message": "POST users"}
