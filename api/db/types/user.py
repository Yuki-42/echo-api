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
from ...models.user import User as PublicUser
from ...models.private import PrivateUser
from ...models.secure import Token, Device

# Constants
__all__ = [
    "User"
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
            last_online=await self.get_last_online(),
            is_online=await self.get_is_online(),
            is_banned=await self.get_is_banned(),
            is_verified=await self.get_is_verified(),
            tokens=await self.get_tokens(),
            password_last_updated=await self.get_password_last_updated()
        )

    async def get_email(self) -> str:
        """
        Get email.

        Returns:
            str: Email.
        """
        # Get email
        with self.id_get(
                column=Identifier("email"),
                id=str(self.id)
        ) as cursor:
            cursor: AsyncCursor
            # Get row
            row: DictRow = await cursor.fetchone()

        # Return email
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
        # Get get_username
        with self.id_get(
                column=Identifier("username"),
                id=str(self.id)
        ) as cursor:
            cursor: AsyncCursor
            # Get row
            row: DictRow = await cursor.fetchone()

        # Return username
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
        # Set get_username
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
        with await self.id_get(
                column=Identifier("icon"),
                id=str(self.id)
        ) as cursor:
            cursor: AsyncCursor
            # Get row
            row: DictRow = await cursor.fetchone()

        # Get icon
        icon: UUID = row["icon"]
        print(f"Icon type: {type(icon)}")
        return icon  # TODO: Ensure that this is an actual UUID

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
        # Create new transaction
        raise NotImplementedError("Icon not implemented.")  # TODO: Implement icon property

    async def get_bio(self) -> str:
        """
        Get bio.

        Returns:
            str: Bio.
        """
        # Get bio
        with await self.id_get(
                column=Identifier("bio"),
                id=self.id
        ) as cursor:
            cursor: AsyncCursor

            # Get row
            row: DictRow = await cursor.fetchone()

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

    async def get_last_online(self) -> datetime:
        """
        Get last online.

        Returns:
            datetime: Last online.
        """
        # Get last_online
        with await self.id_get(
                column=Identifier("last_online"),
                id=self.id
        ) as cursor:
            cursor: AsyncCursor

            # Get row
            row: DictRow = await cursor.fetchone()
        return row["last_online"]  # Skip datetime conversion here because postgresql is based

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
        with await self.id_get(
                column=Identifier("is_online"),
                id=self.id
        ) as cursor:
            cursor: AsyncCursor

            # Get row
            row: DictRow = await cursor.fetchone()

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
        # Get is_banned
        with self.id_get(
                column=Identifier("is_banned"),
                id=self.id
        ) as cursor:
            cursor: AsyncCursor

            # Get row
            row: DictRow = await cursor.fetchone()

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
        with self.id_get(
                column=Identifier("is_verified"),
                id=self.id
        ) as cursor:
            cursor: AsyncCursor

            # Get row
            row: DictRow = await cursor.fetchone()

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

    async def get_tokens(self) -> list[Token]:
        """
        Get tokens.

        Returns:
            list: Tokens.
        """
        # Get tokens
        with self.connection.cursor() as cursor:
            cursor: AsyncCursor

            # Get tokens
            await cursor.execute(
                "SELECT * FROM secured.tokens WHERE user_id = %s;",
                [str(self.id)]
            )

            token_data: list[DictRow] = await cursor.fetchall()

        # Get devices
        for token in token_data:
            with self.connection.cursor() as cursor:
                cursor: AsyncCursor

                # Get device
                await cursor.execute(
                    "SELECT * FROM secured.devices WHERE id = %s;",
                    [token["device_id"]]
                )
                device_data: DictRow = await cursor.fetchone()
                token["device"] = Device(
                    id=device_data["id"],
                    created_at=datetime.strptime(device_data["created_at"], "%Y-%m-%d %H:%M:%S.%f"),
                    name=device_data["name"],
                    ip=device_data["ip"],
                    mac=device_data["mac"],
                    lang=device_data["lang"],
                    os=device_data["os"],
                    screen_size=device_data["screen_size"],
                    country=device_data["country"]
                )

        return [
            Token(
                user=self,
                device=Device(
                    id=UUID(token["device_id"]),
                    created_at=datetime.strptime(token["created_at"], "%Y-%m-%d %H:%M:%S.%f"),
                    name=token["name"],
                    ip=token["ip"],
                    mac=token["mac"],
                    lang=token["lang"],
                    os=token["os"],
                    screen_size=token["screen_size"],
                    country=token["country"]
                ),
                token=token["token"],
                last_used=datetime.strptime(token["last_used"], "%Y-%m-%d %H:%M:%S.%f")
            ) for token in token_data
        ]

    async def get_password_last_updated(self) -> datetime:
        """
        Get password last updated.

        Returns:
            datetime: Password last updated.
        """
        # Create cursor
        with self.connection.cursor() as cursor:
            cursor: AsyncCursor

            # Get last updated
            await cursor.execute(
                "SELECT last_updated FROM secured.passwords WHERE user_id = %s;",
                [self.id]
            )

            row: DictRow = await cursor.fetchone()

        return row["last_updated"]
