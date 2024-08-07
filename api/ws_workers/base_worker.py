"""
Contains the base worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

# Local Imports
from ..db import Database

# Constants
__all__ = [
    "BaseWorker",
]


class BaseWorker:
    """
    Base worker class.
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
        """
        self.connection = connection
        self.database = database

    async def run(self) -> None:
        """
        Run the worker.

        Starts the event handle loop for the worker and listens for incoming messages. When an incoming message is received, this method fires a callback to `handle_message`.
        """
        while True:
            try:
                data: dict = await self.connection.receive_json()
            except WebSocketDisconnect:
                await self.connection.close()
                return
            except KeyError:  # This catches the error when the data is not a dictionary.
                await self.connection.send_json(
                    {
                        "error": "Invalid data."
                    }
                )
                continue

            if "action" not in data:
                await self.connection.send_json(
                    {
                        "error": "No action provided."
                    }
                )
                continue

            if not isinstance(data["action"], str):
                await self.connection.send_json(
                    {
                        "error": "Invalid action type."
                    }
                )
                continue

            if data["action"] == "ping":
                await self.connection.send_json(
                    {
                        "action": "pong"
                    }
                )
                continue

            await self.handle_message(data)

    async def handle_message(
            self,
            data: dict
    ) -> None:
        """
        Handle a message.

        Args:
            data (dict): The incoming message data.
        """
        raise NotImplementedError("The `handle_message` method must be implemented in the child class.")
