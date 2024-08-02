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
client: TestClient = TestClient(app)


class TestUsers(TestCase):
    """
    Test the HTTPS API endpoint for users.
    """

    def test_unauthorised_get_users(self):
        """
        Test the GET method for the users endpoint without authorisation.
        """

        response: Response = client.get("/users")
        assert response.status_code == 200
        assert response.json() == {"message": "GET users"}

    def test_post_users(self):
        """
        Test the POST method for the users endpoint.
        """

        response: Response = client.post("/users")
        assert response.status_code == 200
        assert response.json() == {"message": "POST users"}

    def test_put_users(self):
        """
        Test the PUT method for the users endpoint.
        """

        response: Response = client.put("/users")
        assert response.status_code == 200
        assert response.json() == {"message": "PUT users"}

    def test_delete_users(self):
        """
        Test the DELETE method for the users endpoint.
        """

        response: Response = client.delete("/users")
        assert response.status_code == 200
        assert response.json() == {"message": "DELETE users"}