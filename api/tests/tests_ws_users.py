"""
Contains the user WS test endpoints.
"""

# Standard Library Imports
from unittest import IsolatedAsyncioTestCase

# Third Party Imports
from fastapi.testclient import TestClient

# Local Imports
from api.api import app
from api.config import CONFIG

# Constants
__all__ = [
    "TestUserWs"
]


class TestUserWs(IsolatedAsyncioTestCase):
    """
    Test the user WS endpoints.
    """

    def test_user_ws(self) -> None:
        """
        Test that the user endpoint can be connected to.
        """
        # Create test client
        client: TestClient = TestClient(app)

        # Connect to the endpoint
        with client.websocket_connect("/user/") as connection:
            return
