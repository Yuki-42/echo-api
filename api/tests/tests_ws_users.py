"""
Contains the user WS test endpoints.
"""
# Standard Library Imports
from unittest import IsolatedAsyncioTestCase
from uuid import UUID, uuid4
from random import choice as random_choice, randint
from string import printable, ascii_letters, digits, punctuation

# Third Party Imports
from fastapi.testclient import TestClient

# Local Imports
from api.api import app
from api.config import CONFIG

# Constants
__all__ = [
    "TestUserWs"
]


def generate_password(
        num_lowercase: int,
        num_uppercase: int,
        num_number: int,
        num_special: int,
        length: int
) -> str:  # TODO: Make this include all possible characters including random bytes
    """
    Generates a password with the given requirements.

    Args:
        num_lowercase (int): The number of lowercase characters to include.
        num_uppercase (int): The number of uppercase characters to include.
        num_number (int): The number of number characters to include.
        num_special (int): The number of special characters to include.
        length (int): The length of the password.
    """
    # Check that the individual requirements are not greater than the total length
    if num_lowercase + num_uppercase + num_number + num_special > length:
        raise ValueError("The sum of the individual requirements must be less than the total length.")

    # Generate the password
    password: str = (
        f"{random_choice(ascii_letters.lower()) * num_lowercase}"
        f"{random_choice(ascii_letters.upper()) * num_uppercase}"
        f"{random_choice(digits) * num_number}"
        f"{random_choice(punctuation) * num_special}"
    )

    # Pad the password with random text if it is too short
    for _ in range(length - len(password)):
        password += random_choice(printable)

    # Return the password
    return password


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
            password: str = generate_password(
                num_lowercase=CONFIG.user_security.password_require_lowercase,
                num_uppercase=CONFIG.user_security.password_require_uppercase,
                num_number=CONFIG.user_security.password_require_number,
                num_special=CONFIG.user_security.password_require_special_character,
                length=100
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

            print(password)
            print(len(password))

            connection.send_json(user_data)

            # Print the response
            data: dict = connection.receive_json()

            print(data)


