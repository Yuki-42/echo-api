"""
Contains internal user datatype.
"""
# Standard Library Imports
from datetime import datetime
from uuid import UUID

# Third Party Imports
from psycopg import AsyncConnection, AsyncCursor
from psycopg.rows import DictRow
from psycopg.sql import Identifier

# Local Imports
from .base_type import BaseType
from ...models.secure import PrivateUser
from ...models.user import Status, User as PublicUser

# Constants
__all__ = [
    "User",
]


class User(BaseType):
    """
    User datatype.
    """

    def __init__(
            self,
            connection: AsyncConnection,
            row: DictRow,
    ) -> None:
        """
        Initialize User.

        Args:
            connection (AsyncConnection): Connection.
            row (DictRow): Row.
        """
        # Initialize BaseType
        super(User, self).__init__(connection, row)

        self._table_name = Identifier("users")

    async def to_public(self) -> PublicUser:
        """
        Convert to model.

        Returns:
            UserModel: User model.
        """
        return PublicUser(
            id=self.id,
            created_at=self.created_at,
            email=await self.get_email(),
            username=await self.get_username(),
            icon=await self.get_icon(),
            bio=await self.get_bio(),
            status=await self.get_status(),
            last_online=await self.get_last_online(),
            is_online=await self.get_is_online(),
            is_banned=await self.get_is_banned(),
            is_verified=await self.get_is_verified()
        )

    async def to_private(self) -> PrivateUser:
        """
        Convert to private model.

        Returns:
            UserModel: User model.
        """
        return PrivateUser(
            id=self.id,
            created_at=self.created_at,
            email=await self.get_email(),
            username=await self.get_username(),
            icon=await self.get_icon(),
            bio=await self.get_bio(),
            status=await self.get_status(),
            last_online=await self.get_last_online(),
            is_online=await self.get_is_online(),
            is_banned=await self.get_is_banned(),
            is_verified=await self.get_is_verified(),
            tokens=await self.secure.get_tokens(user_id=self.id),
            password_last_updated=await self.get_password_last_updated()
        )

    async def get_email(self) -> str:
        """
        Get email.

        Returns:
            str: Email.
        """
        # Get email
        row: DictRow = await self.id_get(
            column=Identifier("email"),
            id=str(self.id)
        )
        return row["email"]

    async def set_email(
            self,
            value: str
    ) -> None:
        """
        Set email.

        Args:
            value (str): Email.

        Returns:
            None
        """
        # Set email
        await self.id_set(
            column=Identifier("email"),
            id=str(self.id),
            value=value
        )

    async def get_username(self) -> str:
        """
        Get username.

        Returns:
            str: Username.
        """
        # Get username
        row: DictRow = await self.id_get(
            column=Identifier("username"),
            id=str(self.id)
        )
        return row["username"]

    async def set_username(
            self,
            value: str
    ) -> None:
        """
        Set username.

        Args:
            value (str): Username.

        Returns:
            None
        """
        # Set username
        await self.id_set(
            column=Identifier("username"),
            id=str(self.id),
            value=value
        )

    async def get_icon_id(self) -> UUID:
        """
        Get icon.

        Returns:
            UUID: Icon.
        """
        # Get icon
        row: DictRow = await self.id_get(
            column=Identifier("icon"),
            id=str(self.id)
        )
        return row["icon"]

    async def set_icon_id(
            self,
            value: UUID
    ) -> None:
        """
        Set icon.

        Args:
            value (UUID): Icon.

        Returns:
            None
        """
        # Set icon
        await self.id_set(
            column=Identifier("icon"),
            id=str(self.id),
            value=value
        )

    async def get_icon(self):
        """
        Get icon.

        Returns:
            Icon: Icon.
        """

        # Get icon
        icon_id: UUID = await self.get_icon_id()
        return await self.files.id_get(icon_id)

    async def get_bio(self) -> str:
        """
        Get bio.

        Returns:
            str: Bio.
        """
        # Get bio
        row: DictRow = await self.id_get(
            column=Identifier("bio"),
            id=self.id
        )
        return row["bio"]

    async def set_bio(
            self,
            value: str
    ) -> None:
        """
        Set bio.

        Args:
            value (str): Bio.
        """
        # Set bio
        await self.id_set(
            column=Identifier("bio"),
            id=self.id,
            value=value
        )

    async def get_status(self) -> Status:
        """
        Get status.

        Returns:
            Status: Status.
        """
        # Get status
        row: DictRow = await self.id_get(
            column=Identifier("status"),
            id=self.id
        )
        return Status(
            **row["status"]
        )

    async def set_status(
            self,
            value: Status
    ) -> None:
        """
        Set status.

        Args:
            value (Status): Status.
        """
        # Set status
        await self.id_set(
            column=Identifier("status"),
            id=self.id,
            value=value
        )

    async def get_last_online(self) -> datetime:
        """
        Get last online.

        Returns:
            datetime: Last online.
        """
        # Get last_online
        row: DictRow = await self.id_get(
            column=Identifier("last_online"),
            id=self.id
        )
        return row["last_online"]

    async def set_last_online(
            self,
            value: datetime
    ) -> None:
        """
        Set last online.

        Args:
            value (datetime): Last online.
        """
        # Set last_online
        await self.id_set(
            column=Identifier("last_online"),
            id=self.id,
            value=value
        )

    async def get_is_online(self) -> bool:
        """
        Get online status.

        Returns:
            bool: Online status.
        """
        # Get is_online
        row: DictRow = await self.id_get(
            column=Identifier("is_online"),
            id=self.id
        )
        return row["is_online"]

    async def set_is_online(
            self,
            value: bool
    ) -> None:
        """
        Set online status.

        Args:
            value (bool): Online status.
        """
        # Set is_online
        await self.id_set(
            column=Identifier("is_online"),
            id=self.id,
            value=value
        )

    async def get_is_banned(self) -> bool:
        """
        Get ban status.

        Returns:
            bool: Ban status.
        """
        row: DictRow = await self.id_get(
            column=Identifier("is_banned"),
            id=self.id
        )
        return row["is_banned"]

    async def set_is_banned(
            self,
            value: bool
    ) -> None:
        """
        Set ban status.

        Args:
            value (bool): Ban status.
        """
        # Set is_banned
        await self.id_set(
            column=Identifier("is_banned"),
            id=self.id,
            value=value
        )

    async def get_is_verified(self) -> bool:
        """
        Get verified status.

        Returns:
            bool: Verified status.
        """
        # Get is_verified
        row: DictRow = await self.id_get(
            column=Identifier("is_verified"),
            id=self.id
        )
        return row["is_verified"]

    async def set_is_verified(self, value: bool) -> None:
        """
        Set verified status.

        Args:
            value (bool): Verified status.
        """
        # Set is_verified
        await self.id_set(
            column=Identifier("is_verified"),
            id=self.id,
            value=value
        )

    async def get_password_last_updated(self) -> datetime:
        """
        Get password last updated.

        Returns:
            datetime: Password last updated.
        """
        # Create cursor
        async with self.connection.cursor() as cursor:
            cursor: AsyncCursor

            # Get last updated
            await cursor.execute(
                "SELECT last_updated FROM secured.passwords WHERE user_id = %s;",
                [self.id]
            )

            row: DictRow = await cursor.fetchone()

        return row["last_updated"]
