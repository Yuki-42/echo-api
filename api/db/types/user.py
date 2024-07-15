"""
Contains internal user datatype.
"""
# Standard Library Imports
from uuid import UUID
from datetime import datetime

# Third Party Imports
from psycopg2 import connect
from psycopg2.extras import DictRow, DictConnection

# Local Imports
from ...models.user import User as UserModel

# Constants
__all__ = ["User"]


class User(UserModel):
    """
    User datatype.
    """

    _connection: DictConnection

    def __init__(
            self,
            connection: DictConnection,
            row: DictRow,
    ) -> None:
        super().__init__()
        self._connection = connection

        # Set attributes
        self.id = UUID(row["id"])
        self.created_at =
        self.email = row["email"]
        self.username = row["username"]
        self.icon = row["icon"]
        self.bio = row["bio"]
        self.status = row["status"]
        self.last_online = row["last_online"]
        self.is_online = row["is_online"]
        self.is_banned = row["is_banned"]
        self.is_verified = row["is_verified"]
