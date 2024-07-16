"""
Contains Users handler.
"""

# Standard Library Imports
from hashlib import sha1
from os import urandom

# Third Party Imports
from psycopg2.extras import DictConnection, DictRow

# Local Imports
from ...models.user import User as UserModel
from ..types.user import User
from .base_handler import BaseHandler

# Constants
__all__ = ["Users"]


class Users(BaseHandler):
    """
    Users handler.
    """

    def __init__(
            self,
            connection: DictConnection
    ) -> None:
        super(Users, self).__init__(connection)

    def id_get(
            self,
            user_id: str
    ) -> User:
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

        # Return
        return User(self.connection, row)

    def new(
            self,
            email: str,
            username: str
    ) -> User:
        """
        Create a new user.

        Args:
            email (str): User email.
            username (str): User username.

        Returns:
            User: Live user view.
        """
        # Calculate the user's tag (this is a 6 digit number added to the end of their username)
        #
        # The initial tag is calculated by creating a sha1 hash of the user's username and email and taking the first 6 digits
        # If the tag is already in use, rehash the hash with an extra 16 random bytes and try again
        #
        # This is done to prevent users from having the same tag
        tag: int = sha1((email + username).encode()).digest()[:6]

        # Query
        tag_check_query: str = """
        SELECT 1 FROM users WHERE username = %s AND tag = %s;
        """

        # Check if the tag is already in use
        with self.connection.cursor() as cursor:
            while True:
                cursor.execute(tag_check_query, (username, tag))
                if cursor.fetchone():
                    # Tag is in use, rehash
                    tag = sha1((email + username + str(urandom(16))).encode()).digest()[:6]
                else:
                    break

        # Query
        query: str = """
        INSERT INTO users (email, username, tag) VALUES (%s, %s, %s) RETURNING id, created_at;
        """

        # Execute
        with self.connection.cursor() as cursor:
            cursor.execute(query, (email, username, tag))
            row: DictRow = cursor.fetchone()

        # Return
        return User(self.connection, row)
