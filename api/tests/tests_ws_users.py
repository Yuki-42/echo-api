"""
Contains the user WS test endpoints.
"""

# Standard Library Imports
from unittest import IsolatedAsyncioTestCase
from uuid import UUID, uuid4

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
        with client.websocket_connect("/users/") as connection:
            return

    def test_user_new_valid(self) -> None:
        """
        Test that a new valid user can be created.
        """
        # Create test client
        client: TestClient = TestClient(app)

        # Connect to the endpoint
        with client.websocket_connect("/users/") as connection:
            # Generate the user data
            user_id: UUID = uuid4()
            password: str = (
                f"{"a" * CONFIG.user_security.password_require_lowercase}"
                f"{"A" * CONFIG.user_security.password_require_uppercase}"
                f"{"1" * CONFIG.user_security.password_require_number}"
                f"{"!" * CONFIG.user_security.password_require_special_character}"
            )
            # Submit the user data
            user_data: dict = {
                "action": "new",
                "data": {
                    "username": f"test_user_new_valid_{user_id}",
                    "email": f"test_user_new_valid_{user_id}@testing.blackhole",
                    "password": password
                }
            }

            connection.send_json(user_data)



