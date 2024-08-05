"""
Contains the admin WS test endpoints.
"""

# Standard Library Imports
from hashlib import md5
from unittest import IsolatedAsyncioTestCase

# Third Party Imports
from fastapi.testclient import TestClient
from rsa import decrypt
from starlette.testclient import WebSocketTestSession

# Local Imports
from api.api import app
from api.config import CONFIG

# Constants
__all__ = [
    "TestAdminWs"
]


def run_authenticated_test(
        message: dict,
        expected: dict
) -> None:
    """
    Runs a test with data to send and expected responses.
    """
    # Create test client
    client: TestClient = TestClient(app)

    # Connect to the endpoint
    connection: WebSocketTestSession
    with client.websocket_connect("/admin/") as connection:
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

        # Perform test
        connection.send_json(message)

        assert connection.receive_json() == expected


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

        with client.websocket_connect("/admin/") as connection:
            pass

    def test_admin_auth_success(self) -> None:
        """
        Tests the auth flow for admin connection with a successful auth attempt.
        """
        # Create test client
        client: TestClient = TestClient(app)

        # Connect to the endpoint
        connection: WebSocketTestSession
        with client.websocket_connect("/admin/") as connection:
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

    def test_admin_auth_fail(self) -> None:
        """
        Tests the auth flow for admin connection with a failed auth attempt.
        """
        # Create test client
        client: TestClient = TestClient(app)

        # Connect to the endpoint
        connection: WebSocketTestSession
        with client.websocket_connect("/admin/") as connection:
            # Get the challenge
            challenge: bytes = connection.receive_bytes()

            # Decrypt challenge using private key
            challenge = decrypt(challenge, CONFIG.server.owner_private_key)

            # Hash the challenge
            response: bytes = md5(challenge).digest()

            # Reply with the wrong response
            connection.send_bytes(response[::-1])

            # Check auth fail
            assert connection.receive_json() == {"message": "Authentication failed."}

    def test_admin_ping(self) -> None:
        """
        Test the admin WS ping action.
        """
        # Run authenticated test
        run_authenticated_test(
            {"action": "ping"},
            {"action": "pong"}
        )
