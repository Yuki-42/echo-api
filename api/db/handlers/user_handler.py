"""
Contains the Users handler.
"""

# Standard Library Imports
from hashlib import sha1
from os import urandom

# Third Party Imports
from psycopg import AsyncCursor
from psycopg.rows import DictRow
from psycopg.sql import SQL

# Local Imports
from .base_handler import BaseHandler
from .secure_handler import SecureHandler
from ..types.user import User
from ...models.secure import Device

# Constants
__all__ = [
    "UsersHandler"
]


class UsersHandler(BaseHandler):
    """
    Users handler.
    """

    async def id_get(
            self,
            user_id: str
    ) -> User | None:
        """
        Get user by ID.

        Args:
            user_id (str): User ID.

        Returns:
            User: User.
        """
        # Execute
        with self.connection.cursor() as cursor:
            await cursor.execute(
                SQL(
                    r"SELECT id, created_at FROM users WHERE id = %s;  /* Only select the unchanging columns, everything else is grabbed on-request */",
                ),
                [
                    user_id,
                ]
            )
            row: DictRow = await cursor.fetchone()

        if row is None:
            return None

        # Return
        return User(self.connection, row)

    async def email_get(
            self,
            email: str
    ) -> User | None:
        """
        Get user by email.

        Args:
            email (str): User email.

        Returns:
            User: User.
        """
        # Create a cursor
        cursor: AsyncCursor = self.connection.cursor()

        # Execute
        await cursor.execute(
            SQL(
                r"SELECT id, created_at FROM users WHERE email = %s;  /* Only select the unchanging columns, everything else is grabbed on-request */",
            ),
            [
                email
            ]
        )
        row: DictRow = await cursor.fetchone()

        # Kill the cursor
        await cursor.close()

        if row is None:
            return None

        # Return
        return User(self.connection, row)

    async def new(
            self,
            email: str,
            username: str,
            password: str
    ) -> User:
        """
        Create a new user.

        Args:
            email (str): User email.
            username (str): User username.
            password (str): User password.

        Returns:
            User: Live user view.
        """
        # Hash the password
        password = SecureHandler.hash_password(password)  # This overwrites the value in memory

        # Calculate the user's tag (this is a 6 digit number added to the end of their username)
        #
        # The initial tag is calculated by creating a sha1 hash of the user's username and email and taking the first 6 digits
        # If the tag is already in use, rehash the hash with an extra 16 random bytes and try again
        #
        # This is done to prevent users from having the same tag
        tag: int = int.from_bytes(sha1((email + username).encode()).digest())

        # Strip tag digits
        tag = int(str(tag)[:6])

        # Check if the tag is already in use
        with self.connection.cursor() as cursor:
            while True:
                await cursor.execute(
                    SQL(
                        "SELECT 1 FROM users WHERE username = %s AND tag = %s;"
                    ),
                    [
                        username,
                        tag,
                    ]
                )
                if await cursor.fetchone():
                    # Tag is in use, rehash
                    tag = int.from_bytes(sha1((email + username + str(urandom(16))).encode()).digest())

                    # Strip tag digits
                    tag = int(str(tag)[:6])
                else:
                    break

        # Execute
        with self.connection.cursor() as cursor:
            await cursor.execute(
                SQL(
                    "INSERT INTO users (email, username, tag) VALUES (%s, %s, %s) RETURNING *;"
                ),
                [
                    email,
                    username,
                    tag
                ]
            )
            row: DictRow = await cursor.fetchone()

        # Add user password
        await self.secure.set_password(
            row["id"],
            password
        )

        # Return
        return User(self.connection, row)

    def session_verify(
            self,
            email: str,
            token: str,
            device: Device  # This relies on the client submitting the device information, making it trivial to fake
    ) -> User | None:
        """
        Login a user.

        Args:
            email (str): User email.
            token (str): User access token.
            device (Device): Device for the token.

        Returns:
            User: Live user view.
        """
