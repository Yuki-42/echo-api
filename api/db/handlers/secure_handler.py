"""
Contains the secure handler.
"""

# Standard Library Imports

# Third Party Imports
from psycopg import AsyncCursor
from psycopg.sql import SQL

# Local Imports
from .base_handler import BaseHandler
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
            user_id: str,
            password: str
    ) -> None:
        """
        Sets a user's password.

        Args:
            user_id (str): User ID.
            password (str): Password.
        """

        # Hash password
        password: str = self.hash_password(password)  # Overwrite password with hashed password

        # Get cursor
        cursor: AsyncCursor
        with self.connection.cursor() as cursor:
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
