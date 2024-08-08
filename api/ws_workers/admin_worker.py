"""
Contains the WS Admin Worker.
"""

# Standard Library Imports

# Third Party Imports
from pydantic import ValidationError

# Local Imports
from .base_worker import BaseWorker
from ..db.exceptions import UserDoesNotExist
from ..db.types.user import User
from ..models.user import User as PublicUser
from ..models.validation.admin import DeleteUserInput, GetUsersInput

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
                await self._get_users(data)
            case "get_user":
                await self._get_user(data)
            case "delete_user":
                await self._delete_user(data)
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

        Args:
            data (dict): Data.
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

    async def _get_user(
            self,
            data: dict
    ) -> None:
        """
        Get a user.

        Args:
            data (dict): Data.
        """

    async def _delete_user(
            self,
            data: dict
    ) -> None:
        """
        Delete a user.

        Args:
            data (dict): Data.
        """
        # Verify input model
        try:
            data: DeleteUserInput = DeleteUserInput(**data)
        except ValidationError:
            await self.connection.send_json(
                {"error": "Invalid data."}
            )
            return

        # Delete user
        try:
            await self.database.users.delete(
                data.data.id
            )
        except UserDoesNotExist:
            await self.connection.send_json(
                {"error": "User does not exist."}
            )
            return

        # Send success
        await self.connection.send_json(
            {
                "action": "delete_user",
                "data": {"success": True}
            }
        )

