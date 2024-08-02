"""
Contains database connection information and shared handlers.
"""

# Standard Library Imports
from typing import Type

# Third Party Imports
from psycopg import AsyncConnection
from psycopg.rows import dict_row

# Local Imports
from .handlers import *
from .handlers.secure_handler import SecureHandler
from ..config.config import Config

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

    @classmethod
    async def new(
            cls,
            config: Config
    ) -> "Database":
        self = cls()
        self.config = config

        # Connect handlers
        self.users = UsersHandler(await self._new_connection())
        self.secure = SecureHandler(await self._new_connection())

        # Add handlers to list
        self.handlers = [
            self.users,
            self.secure
        ]

        return self

    async def _new_connection(self) -> AsyncConnection:
        """
        Create a new database connection.

        Returns:
            DictConnection: Database connection.
        """
        connection: AsyncConnection = await AsyncConnection.connect(
            dbname=self.config.db.name,
            user=self.config.db.user,
            password=self.config.db.password,
            host=self.config.db.host,
            port=self.config.db.port,
            row_factory=dict_row
        )
        await connection.set_autocommit(True)
        assert type(connection) is AsyncConnection
        return connection

    async def close(self) -> None:
        """
        Close all handlers.
        """
        for handler in self.handlers:
            handler.close()
