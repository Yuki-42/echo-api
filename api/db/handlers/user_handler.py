"""
Contains the Users handler.
"""

# Standard Library Imports
from hashlib import sha1
from os import urandom
from uuid import UUID

# Third Party Imports
from psycopg import AsyncCursor
from psycopg.rows import DictRow
from psycopg.sql import SQL

# Local Imports
from ..exceptions.users import UserAlreadyExists, UserDoesNotExist
from .base_handler import BaseHandler
from .secure_handler import SecureHandler
from ..types.user import User

# Constants
__all__ = [
    "UsersHandler",
]


class UsersHandler(BaseHandler):
    """
    Users handler.
    """

    async def id_exists(
            self,
            id: UUID
    ) -> bool:
        """
        Checks if the user exists. Is **slightly** faster than fetching the user.

        Args:
            id (UUID): User ID.

        Returns:
            bool: User exists.
        """
        # Create a cursor
        async with self.connection.cursor() as cursor:
            # Execute
            await cursor.execute(
                SQL(
                    r"SELECT 1 FROM users WHERE id = %s;",
                ),
                [
                    str(id),
                ]
            )
            return bool(await cursor.fetchone())

    async def email_exists(
            self,
            email: str
    ) -> bool:
        """
        Checks if the user exists. Is **slightly** faster than fetching the user.

        Args:
            email (str): User email.

        Returns:
            bool: User exists.
        """
        # Create a cursor
        async with self.connection.cursor() as cursor:
            # Execute
            await cursor.execute(
                SQL(
                    r"SELECT 1 FROM users WHERE email = %s;",
                ),
                [
                    email,
                ]
            )
            return bool(await cursor.fetchone())

    async def id_get(
            self,
            id: UUID
    ) -> User | None:
        """
        Get user by ID.

        Args:
            id (str): User ID.

        Raises:
            UserDoesNotExist: Requested user does not exist.

        Returns:
            User: User.
        """
        # Create a cursor
        cursor: AsyncCursor
        with self.connection.cursor() as cursor:
            await cursor.execute(
                SQL(
                    r"SELECT id, created_at FROM users WHERE id = %s;  /* Only select the unchanging columns, everything else is grabbed on-request */",
                ),
                [
                    str(id),
                ]
            )
            row: DictRow = await cursor.fetchone()

        if row is None:
            raise UserDoesNotExist(id)

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

        Raises:
            UserDoesNotExist: Requested user does not exist.

        Returns:
            User: User.
        """
        cursor: AsyncCursor
        # Create a cursor
        async with self.connection.cursor() as cursor:
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
            raise UserDoesNotExist(email)

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

        Raises:
            UserAlreadyExists: A user already exists with that email.

        Returns:
            User: Live user view.
        """
        # Hash the password
        password = SecureHandler.hash_password(password)  # This overwrites the value in memory

        # Check if the user exists by email
        if await self.email_exists(email):
            raise UserAlreadyExists(email)

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
        async with self.connection.cursor() as cursor:
            cursor: AsyncCursor
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
        async with self.connection.cursor() as cursor:
            cursor: AsyncCursor
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

    async def session_verify(
            self,
            email: str,
            token: str
    ) -> User | None:
        """
        Login a user.

        Args:
            email (str): User email.
            token (str): User access token.

        Returns:
            User: Live user view.
        """

    async def get(
            self,
            page: int,
            page_size: int
    ) -> list[User]:
        """
        Get users.

        Args:
            page (int): Page number.
            page_size (int): Page size.

        Returns:
            list[User]: List of users.
        """
        # Create a cursor
        cursor: AsyncCursor
        async with self.connection.cursor() as cursor:
            # Execute
            await cursor.execute(
                SQL(
                    r"SELECT id, created_at FROM users ORDER BY created_at DESC LIMIT %s OFFSET %s;",
                ),
                [
                    page_size,
                    page * page_size
                ]
            )
            rows: list[DictRow] = await cursor.fetchall()

        # Return
        return [User(self.connection, row) for row in rows]
