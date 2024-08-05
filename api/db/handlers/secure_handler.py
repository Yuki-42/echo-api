"""
Contains the secure handler.
"""

# Standard Library Imports
from uuid import UUID

# Third Party Imports
from psycopg import AsyncCursor
from psycopg.rows import DictRow
from psycopg.sql import SQL

# Local Imports
from .base_handler import BaseHandler
from ...models.secure import Token, Password, Device
from ...security.scheme import crypt_context

# Constants


class SecureHandler(BaseHandler):
    """
    Secure handler.
    """

    @staticmethod
    def hash_password(
            password: str
    ) -> str:
        """
        Hash a password.

        Args:
            password (str): Password.

        Returns:
            str: Hashed password.
        """
        return crypt_context.hash(password)

    @staticmethod
    def verify_password(
            password: str,
            hashed_password: str
    ) -> bool:
        """
        Verify a password.

        Args:
            password (str): Password.
            hashed_password (str): Hashed password.

        Returns:
            bool: Verification.
        """
        return crypt_context.verify(password, hashed_password)

    async def set_password(
            self,
            user_id: UUID,
            password: str
    ) -> None:
        """
        Sets a user's password.

        Args:
            user_id (UUID): User ID.
            password (str): Password.
        """

        # Hash password
        password: str = self.hash_password(password)  # Overwrite password with hashed password

        # Get cursor
        cursor: AsyncCursor
        async with self.connection.cursor() as cursor:
            # Remove old password
            await cursor.execute(
                SQL(
                    r"DELETE FROM secured.passwords WHERE user_id = %s;",
                ),
                [
                    user_id,
                ]
            )

            # Insert new password
            await cursor.execute(
                SQL(
                    r"INSERT INTO secured.passwords (user_id, password) VALUES (%s, %s);",
                ),
                [
                    user_id,
                    password,
                ]
            )

    async def get_password(
            self,
            user_id: UUID
    ) -> Password | None:
        """
        Gets the hash of a user's password from the database.

        Args:
            user_id (UUID): User ID.

        Returns:
            str: Hashed password.
        """
        cursor: AsyncCursor
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                SQL(
                    r"SELECT password, last_updated FROM secured.passwords WHERE user_id = %s;",
                ),
                [
                    user_id,
                ]
            )
            row: dict = await cursor.fetchone()

        if row is None:
            return None

        return Password(
            hash=row["password"],
            last_updated=row["last_updated"]
        )

    async def get_device(
            self,
            device_id: UUID
    ) -> Device:
        """
        Get a device.

        Args:
            device_id (UUID): Device id.

        Returns:
            Device: Device.
        """
        cursor: AsyncCursor
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "SELECT * FROM secured.devices WHERE id = %s;",
                [device_id]
            )
            row: DictRow = await cursor.fetchone()

        return Device(
            id=row["id"],
            created_at=row["created_at"],
            name=row["name"],
            ip=row["ip"],
            mac=row["mac"],
            lang=row["lang"],
            os=row["os"],
            screen_size=row["screen_size"],
            country=row["country"]
        )

    async def new_token(
            self,
            user_id: UUID
    ) -> Token:
        """
        Build a new authentication token. This will also create a new device if the device does not exist.

        Args:
            user_id (UUID): User ID.

        Returns:
            Token: Token.
        """
        raise NotImplemented("New token method not implemented yet.")

    async def get_tokens(
            self,
            user_id: UUID
    ) -> list[Token]:
        """
        Gets the tokens of a user.

        Args:
            user_id (UUID): User ID.

        Returns:
            list[str]: Tokens.
        """
        # Get tokens
        async with self.connection.cursor() as cursor:
            cursor: AsyncCursor

            # Get tokens
            await cursor.execute(
                "SELECT * FROM secured.tokens WHERE user_id = %s;",
                [str(user_id)]
            )

            token_data: list[DictRow] = await cursor.fetchall()

        # Get devices
        for token in token_data:
            token["device"] = await self.get_device(token["device_id"])

        return [
            Token(
                user=await self.users.id_get(user_id),
                device=token["device"],
                token=token["token"],
                last_used=token["last_used"]
            ) for token in token_data
        ]
