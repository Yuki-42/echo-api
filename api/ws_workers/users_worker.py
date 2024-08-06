"""
Contains the WS Users Worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

# Local Imports
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

    async def run(self) -> None:
        """
        Run the worker.
        """
        while True:
            try:
                data: dict = await self.connection.receive_json()
            except WebSocketDisconnect:
                await self.connection.close()
                return

            if "action" not in data:
                await self.connection.send_json(
                    {
                        "error": "No action provided."
                    }
                )
                continue

            action: str = data["action"]

            match action:
                case "new":
                    await self.new_user(data)
                case "login":
                    await self.login_user(data)
                case "logout":
                    await self.logout_user(data)

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