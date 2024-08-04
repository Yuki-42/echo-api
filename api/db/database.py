"""
Contains database connection information and shared handlers.
"""

# Standard Library Imports
from typing import Type

# Third Party Imports
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

# Local Imports
from .handlers import *
from .handlers.secure_handler import SecureHandler
from ..config.config import CONFIG

# Constants
__all__ = [
    "Database"
]

# Create connection pool for database
connection_pool = AsyncConnectionPool(
    conninfo=f"dbname={CONFIG.db.name} user={CONFIG.db.user} password={CONFIG.db.password} host={CONFIG.db.host} port={CONFIG.db.port}",
    open=True,
    min_size=4,
    max_size=10,
    timeout=10,
)


class Database:
    """
    Database connection group.
    """

    # List of running handlers
    handlers: list[Type[any]]  # TODO: Get correct typing for this

    # Handlers
    users: UsersHandler
    secure: SecureHandler

    @classmethod
    async def new(
            cls
    ) -> "Database":
        self = cls()

        # Connect handlers
        self.users = UsersHandler(await self._new_connection())
        self.secure = SecureHandler(await self._new_connection())

        # Add handlers to list
        self.handlers = [
            self.users,
            self.secure
        ]

        return self

    @staticmethod
    async def _new_connection() -> AsyncConnection:
        """
        Create a new database connection.

        Returns:
            DictConnection: Database connection.
        """
        connection = await connection_pool.connection(
            row_factory=dict_row
        )
        await connection.set_autocommit(True)
        assert type(connection) is AsyncConnection
        return connection

    async def close(self) -> None:
        """
        Close the database connection.
        """
        for handler in self.handlers:
            await handler.close()

