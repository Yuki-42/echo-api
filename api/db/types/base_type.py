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
from ..base_db_interactor import BaseDbInteractor

# Constants
__all__ = [
    "BaseType",
]


class BaseType(BaseDbInteractor):
    """
    Base DB type.

    Provides the connection attribute.
    """
    _table_name: Identifier

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
        # Initialize BaseDbInteractor
        super(BaseType, self).__init__(connection)

        # Set attributes
        self.id = row["id"]
        self.created_at = row["created_at"]

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
                    r"SELECT {COLUMN} FROM {TABLE} WHERE {KEY} = %s;"
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
                    r"UPDATE {TABLE} SET {COLUMN} = %s WHERE {KEY} = %s;"
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
