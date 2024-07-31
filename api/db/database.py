"""
Contains database connection information and shared handlers.
"""

# Standard Library Imports
from typing import Type

# Third Party Imports
from psycopg import connect, AsyncConnection
from psycopg.rows import DictRow

# Local Imports
from .handlers import *
from .handlers.secure_handler import SecureHandler
from ..internals.config import Config

# Constants
__all__ = [
    "Database"
]


class Database:
    """
    Database connection group.
    """
    config: Config

    # List of running handlers
    handlers: list[Type[any]]  # TODO: Get correct typing for this

    # Handlers
    users: UsersHandler
    secure: SecureHandler

    def __init__(
            self,
            config: Config
    ) -> None:
        self.config = config

        # Connect handlers
        self.users = UsersHandler(self._new_connection())
        self.secure = SecureHandler(self._new_connection())

        # Add handlers to list
        self.handlers = [
            self.users,
            self.secure
        ]

    def _new_connection(self) -> AsyncConnection:
        """
        Create a new database connection.

        Returns:
            DictConnection: Database connection.
        """
        connection: AsyncConnection = connect(
            dbname=self.config.db.name,
            user=self.config.db.user,
            password=self.config.db.password,
            host=self.config.db.host,
            port=self.config.db.port,
            row_factory=DictRow
        )
        connection.autocommit = True
        return connection

    async def close(self) -> None:
        """
        Close all handlers.
        """
        for handler in self.handlers:
            handler.close()

    def __del__(self) -> None:
        """
        Close all handlers.
        """
        self.close()
