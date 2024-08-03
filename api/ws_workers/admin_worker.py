"""
Contains the WS Admin Worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket

# Local Imports
from ..db import Database

# Constants
__all__ = [
    "AdminWorker"
]


class AdminWorker:
    """
    Worker to handle admin WebSocket connections.
    """
    connection: WebSocket
    database: Database

    def __init__(
            self,
            connection: WebSocket,
            database: Database
    ) -> None:
        """
        Initialise the worker.

        Args:
            connection (WebSocket): WebSocket connection.
            database (Database): Database connection.
        """
        self.connection = connection
        self.database = database

    async def run(self) -> None:
        """
        Run the worker.
        """
        while True:
            data: dict = await self.connection.receive_json()

            # Ensure that the base level spec is present
            if "action" not in data:
                await self.connection.send_json(
                    {"error": "No action provided."}
                )
                continue

            # Match action
            action: str = data.get("action")

            match action:
                case "get_users":
                    await self.connection.send_json(
                        {"action": "pong"}
                    )
                case "delete_user":
                    await self.connection.close()
                    break
                case _:
                    await self.connection.send_json(
                        {"error": "Invalid action."}
                    )

    async def _get_users(self) -> None:
        """
        Get users.
        """
        pass

    async def _delete_user(self) -> None:
        """
        Delete a user.
        """
        pass

