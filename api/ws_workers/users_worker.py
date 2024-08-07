"""
Contains the WS Users Worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket
from pydantic import ValidationError
from starlette.websockets import WebSocketDisconnect

# Local Imports
from ..db.types.user import User
from ..config import CONFIG
from ..models import PrivateUser, User as PublicUser
from ..models.validation import RegisterInput, LoginInput, RegisterInputData, LoginInputData
from .base_worker import BaseWorker
from ..db import Database

# Constants
__all__ = [
    "UsersWorker"
]


class UsersWorker(BaseWorker):
    """
    Worker to handle user WebSocket connections.
    """
    _database: Database

    def __init__(
            self,
            connection: WebSocket,
            database: Database
    ) -> None:
        """
        Initialise the worker.
        """
        super().__init__(connection)
        self._database = database

    async def handle_message(
            self,
            data: dict
    ) -> None:
        """
        Handle a message from the client.

        Args:
            data (dict): The data to handle.
        """
        action: str = data["action"]

        match action:
            case "new":
                await self.new_user(data)
            case "login":
                await self.login_user(data)
            case "logout":
                await self.logout_user(data)
            case "me":
                await self.me(data)
            case "details":
                await self.details(data)

    async def new_user(
            self,
            data: dict
    ) -> None:
        """
        Create a new user.

        Args:
            data (dict): The data to create the user with.

        Returns:
            None
        """
        # Validate data
        try:
            data: RegisterInput = RegisterInput(**data)
        except ValidationError as e:
            await self.connection.send_json(
                {
                    "action": "new",
                    "error": e.errors()
                }
            )
            return

        # Strip the action from the data
        data: RegisterInputData = data.data

        # Do user password checks before anything else to minimise in-flight time for password
        if len(data.password) > CONFIG.user_security.password_maximum_length or len(data.password) < CONFIG.user_security.password_minimum_length:
            await self.connection.send_json(
                {
                    "action": "new",
                    "error": "password_length_invalid",
                    "data": {
                        "max_len": CONFIG.user_security.password_maximum_length,
                        "min_len": CONFIG.user_security.password_minimum_length
                    }
                }
            )
            return

        # Count numbers of each character type
        uppercase: int = 0
        lowercase: int = 0
        number: int = 0
        special: int = 0

        for char in data.password:
            if char.isupper():
                uppercase += 1
            elif char.islower():
                lowercase += 1
            elif char.isdigit():
                number += 1
            else:
                special += 1

        if uppercase < CONFIG.user_security.password_require_uppercase:
            await self.connection.send_json(
                {
                    "action": "new",
                    "error": "password_uppercase_invalid",
                    "data": {
                        "condition": "uppercase_count",
                        "minimum_value": CONFIG.user_security.password_require_uppercase
                    }
                }
            )

        if lowercase < CONFIG.user_security.password_require_lowercase:
            await self.connection.send_json(
                {
                    "action": "new",
                    "error": "password_lowercase_invalid",
                    "data": {
                        "condition": "lowercase_count",
                        "minimum_value": CONFIG.user_security.password_require_lowercase
                    }
                }
            )

        if number < CONFIG.user_security.password_require_number:
            await self.connection.send_json(
                {
                    "action": "new",
                    "error": "password_number_invalid",
                    "data": {
                        "condition": "number_count",
                        "minimum_value": CONFIG.user_security.password_require_number
                    }
                }
            )

        if special < CONFIG.user_security.password_require_special_character:
            await self.connection.send_json(
                {
                    "action": "new",
                    "error": "password_special_invalid",
                    "data": {
                        "condition": "special_count",
                        "minimum_value": CONFIG.user_security.password_require_special_character
                    }
                }
            )

        # Check if the user exists
        user: User = await self._database.users.email_get(data.email)

        if user is not None:
            await self.connection.send_json(
                {
                    "action": "new",
                    "error": "user_exists"
                }
            )
            return

        # Create user
        user: User = await self._database.users.new(data.email, data.username, data.password)

        # Convert to private and send
        user_data: PublicUser = await user.to_public()

        # Construct the response
        await self.connection.send_json(
            {
                "action": "new",
                "data": user_data.model_dump(mode="json")
            }
        )

    async def login_user(
            self,
            data: dict
    ) -> None:
        """
        Log a user in.

        Args:
            data (dict): The data to log the user in with.

        Returns:
            None
        """

    async def logout_user(
            self,
            data: dict
    ) -> None:
        """
        Log a user out.

        Args:
            data (dict): The data to log the user out with.

        Returns:
            None
        """

    async def me(
            self,
            data: dict
    ) -> None:
        """
        Gets information about the current user. Shorthand for details.

        Args:
            data (dict): The data to get the user with.

        Returns:
            None
        """

    async def details(
            self,
            data: dict
    ) -> None:
        """
        Get details about a user.

        Args:
            data (dict): The data to get the user with.

        Returns:
            None
        """
