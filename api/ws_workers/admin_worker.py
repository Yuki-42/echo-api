"""
Contains the WS Admin Worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

# Local Imports
from .base_worker import BaseWorker

# Constants
__all__ = [
    "AdminWorker",
]


class AdminWorker(BaseWorker):
    """
    Worker to handle admin WebSocket connections.
    """

    async def handle_message(
            self,
            data: dict
    ) -> None:
        """
        Handle a message from the client.

        Args:
            data (dict): The data to handle.
        """
        # Match action
        action: str = data.get("action")

        match action:

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
