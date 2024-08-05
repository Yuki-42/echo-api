"""
Contains the WS Admin Worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

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

    def __init__(
            self,
            connection: WebSocket
    ) -> None:
        """
        Initialise the worker.

        Args:
            connection (WebSocket): WebSocket connection.
        """
        self.connection = connection

    async def run(self) -> None:
        """
        Run the worker.
        """
        while True:
            try:
                data: dict = await self.connection.receive_json()  # THIS IS THROWING A 1000 ERROR. This means that the websocket is already closed
            except WebSocketDisconnect:
                await self.connection.close()
                return  # Gracefully handle disconnect

            # Ensure that the base level spec is present
            if "action" not in data:
                await self.connection.send_json(
                    {"error": "No action provided."}
                )
                continue

            # Match action
            action: str = data.get("action")

            match action:
                case "ping":
                    await self.connection.send_json(
                        {"action": "pong"}
                    )
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
