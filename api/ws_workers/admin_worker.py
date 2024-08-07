"""
Contains the WS Admin Worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket
from pydantic import ValidationError
from starlette.websockets import WebSocketDisconnect

# Local Imports
from .base_worker import BaseWorker
from ..db.types.user import User
from ..models.validation.admin import GetUsersInput, GetUsersInputData
from ..models.user import User as PublicUser

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
            case "get_users":
                await self._get_users(
                    data
                )
            case "delete_user":
                await self._delete_user()
            case _:
                await self.connection.send_json(
                    {"error": "Invalid action."}
                )

    async def _get_users(
            self,
            data: dict
    ) -> None:
        """
        Get users.
        """
        # Verify input model
        try:
            data: GetUsersInput = GetUsersInput(**data)
        except ValidationError:
            await self.connection.send_json(
                {"error": "Invalid data."}
            )
            return

        # Get users
        users: list[User] = await self.database.users.get(
            data.data.page,
            data.data.page_size
        )
        users: list[PublicUser] = [await user.to_public() for user in users]

        # Send users
        await self.connection.send_json(
            {
                "action": "users",
                "data": [user.model_dump(mode="json") for user in users]
            }
        )

    async def _delete_user(self) -> None:
        """
        Delete a user.
        """
        # Verify input model
