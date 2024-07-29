"""
Contains Users handler.
"""

# Standard Library Imports
from hashlib import sha1
from os import urandom

# Third Party Imports
from passlib.hash import pbkdf2_sha512
from psycopg2.extras import DictConnection, DictRow

# Local Imports
from .base_handler import BaseHandler
from ..types.user import User

# Constants
__all__ = [
    "Users"
]


class Users(BaseHandler):
    """
    Users handler.
    """

    def __init__(
            self,
            connection: DictConnection
    ) -> None:
        """
        Initialize the Users handler.

        Args:
            connection (DictConnection): Database connection.
        """
        super(Users, self).__init__(connection)

    def id_get(
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
        # Query
        query = """
        SELECT id, created_at FROM users WHERE id = %s;  /* Only select the unchanging columns, everything else is grabbed on-request */
        """

        # Execute
        with self.connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            row: DictRow = cursor.fetchone()

        if row is None:
            return None

        # Return
        return User(self.connection, row)

    def email_get(
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

        # Execute
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, created_at FROM users WHERE email = %s;  /* Only select the unchanging columns, everything else is grabbed on-request */",
                [email]
            )
            row: DictRow = cursor.fetchone()

        if row is None:
            return None

        # Return
        return User(self.connection, row)

    def new(
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
        password = pbkdf2_sha512.hash(password)  # This overwrites the value in memory

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
                cursor.execute("SELECT 1 FROM users WHERE username = %s AND tag = %s;", (username, tag))
                if cursor.fetchone():
                    # Tag is in use, rehash
                    tag = int.from_bytes(sha1((email + username + str(urandom(16))).encode()).digest())

                    # Strip tag digits
                    tag = int(str(tag)[:6])
                else:
                    break

        # Execute
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (email, username, tag) VALUES (%s, %s, %s) RETURNING *;", (email, username, tag))
            row: DictRow = cursor.fetchone()

        # Add user password
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO secured.passwords (user_id, password) VALUES (%s, %s);", (row["id"], password))

        # Return
        return User(self.connection, row)
