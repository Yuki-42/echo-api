"""
Base DB type.
"""

# Standard Library Imports
from datetime import datetime
from uuid import UUID

# Third Party Imports
from psycopg import AsyncConnection, AsyncCursor
from psycopg.rows import DictRow
from psycopg.sql import Identifier, SQL

# Local Imports

# Constants
__all__ = [
    "BaseType"
]


class BaseType:
    """
    Base DB type.

    Provides the connection attribute.
    """
    _table_name: Identifier
    _connection: AsyncConnection

    id: UUID
    created_at: datetime

    def __init__(
            self,
            connection: AsyncConnection,
            row: DictRow
    ) -> None:
        """
        Initialize BaseType.
        """
        self._connection = connection

        # Set attributes
        self.id = row["id"]
        self.created_at = row["created_at"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    @property
    def connection(self) -> AsyncConnection:
        """
        Get connection.

        Returns:
            DictConnection: Database connection.
        """

        if not self._connection:
            raise AttributeError("Connection not set.")

        return self._connection

    async def id_get(
            self,
            column: Identifier,
            id: any
    ) -> DictRow:
        """
        Gets a the value present in a column from the database using the current object's ID.

        Args:
            column (Identifier): Column name.
            id (any): ID.

        Returns:
            cursor (DictCursor): Cursor.
        """
        row: DictRow = await self.get(
            column=column,
            key=Identifier("id"),
            key_value=id
        )
        return row

    async def get(
            self,
            column: Identifier,
            key: Identifier,
            key_value: any
    ) -> DictRow:
        """
        Gets the value of a column from the database.

        Args:
            column (Identifier): Column name.
            key (Identifier): Key column name.
            key_value (any): Key column value.

        Returns:
            cursor (DictRow): Cursor.
        """
        # Get cursor
        cursor: AsyncCursor
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                SQL(
                    r"SELECT {column} FROM {table} WHERE {key} = %s;"
                ).format(
                    column=column,
                    table=self._table_name,
                    key=key
                ),
                [
                    str(key_value),
                ]
            )

            # Get the row
            row: DictRow = await cursor.fetchone()

        return row

    async def id_set(
            self,
            column: Identifier,
            value: any,
            id: any
    ) -> None:
        """
        Sets the value of a column in the database using the current object's ID.

        Args:
            column (Identifier): Column name.
            value (any): Value.
            id (any): ID.

        Returns:
            None
        """
        await self.set(
            column=column,
            value=value,
            key=Identifier("id"),
            key_value=id
        )

    async def set(
            self,
            column: Identifier,
            value: any,
            key: Identifier,
            key_value: any
    ) -> None:
        """
        Sets the value of a column in the database.

        Args:
            column (Identifier): Column name.
            value (any): Value.
            key (Identifier): Key column name.
            key_value (any): Key column value.

        Returns:
            None
        """
        cursor: AsyncCursor
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                SQL(
                    r"UPDATE {table} SET {column} = %s WHERE {key} = %s;"
                ).format(
                    column=column,
                    table=self._table_name,
                    key=key
                ),
                [
                    value,
                    key_value
                ]
            )

    """
    External handler methods
    """

    @property
    def users(self):  # This is a great example of how to use a property to create a handler. (I think)
        """
        Get users handler.
        """
        from ..handlers.user_handler import UsersHandler
        return UsersHandler(self.connection)

    @property
    def secure(self):
        """
        Get secure handler.
        """
        from ..handlers.secure_handler import SecureHandler
        return SecureHandler(self.connection)
