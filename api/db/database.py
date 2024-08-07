"""
Contains database connection information and shared handlers.
"""

# Standard Library Imports

# Third Party Imports
from psycopg import AsyncConnection
from psycopg.rows import dict_row

# Local Imports
from .handlers import *
from .handlers.secure_handler import SecureHandler
from ..config.config import CONFIG

# Constants
__all__ = [
    "Database",
]


class Database:
    """
    Database connection group.
    """
    # Connection
    _connection: AsyncConnection

    # Handlers
    users: UsersHandler
    secure: SecureHandler

    @classmethod
    async def new(
            cls
    ) -> "Database":
        self = cls()

        try:
            # Get connection for this instance
            self._connection = await AsyncConnection.connect(
                host=CONFIG.db.host,
                port=CONFIG.db.port,
                user=CONFIG.db.user,
                password=CONFIG.db.password,
                dbname=CONFIG.db.name,
                row_factory=dict_row
            )
            await self._connection.set_autocommit(True)
            assert type(self._connection) is AsyncConnection

            # Connect handlers
            self.users = UsersHandler(self._connection)
            self.secure = SecureHandler(self._connection)

            # Add handlers to list
            self.handlers = [
                self.users,
                self.secure
            ]

            yield self
        finally:
            await self.close()

    async def close(self) -> None:
        """
        Close the database connection.
        """
        await self._connection.close()

