"""
Contains the admin WS test endpoints.
"""

# Standard Library Imports
from hashlib import md5
from rsa import decrypt
from unittest import IsolatedAsyncioTestCase, TestCase

# Third Party Imports
from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession

# Local Imports
from api.api import app
from api.config import CONFIG

# Constants
__all__ = [
    "TestAdminWs"
]


class TestAdminWs(IsolatedAsyncioTestCase):
    """
    Test the admin WS endpoints.
    """

    def test_admin_connect(self) -> None:
        """
        Test the admin WS connection.
        """
        # Create a test client
        client: TestClient = TestClient(app)

        # Make the request
        connection: WebSocketTestSession

        with client.websocket_connect("/admin/ws") as connection:
            pass

    def test_admin_auth(self) -> None:
        """
        Tests the auth flow for admin connection.
        """
        # Create test client
        client: TestClient = TestClient(app)

        # Connect to the endpoint
        connection: WebSocketTestSession
        with client.websocket_connect("/admin/ws") as connection:
            # Get the challenge
            challenge: bytes = connection.receive_bytes()

            # Decrypt challenge using private key
            challenge = decrypt(challenge, CONFIG.server.owner_private_key)

            # Hash the challenge
            response: bytes = md5(challenge).digest()

            # Reply with the response
            connection.send_bytes(response)

            # Check auth success
            assert connection.receive_json() == {"message": "Authenticated."}
