"""
Base DB type.
"""

# Standard Library Imports

# Third Party Imports
from psycopg2.extras import DictConnection, DictCursor
from psycopg2.sql import Identifier, SQL

# Local Imports

# Constants
__all__ = ["BaseType"]


class BaseType:
    """
    Base DB type.

    Provides the connection attribute.
    """
    _table_name: Identifier
    _connection: DictConnection

    def __init__(self) -> None:
        """
        Initialize BaseType.
        """

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    @property
    def connection(self) -> DictConnection:
        """
        Get connection.

        Returns:
            DictConnection: Database connection.
        """

        if not self._connection:
            raise AttributeError("Connection not set.")

        return self._connection

    def id_get(
            self,
            column: Identifier,
            id: any
    ) -> DictCursor:
        """
        Gets a the value present in a column from the database using the current object's ID.

        Args:
            column (Identifier): Column name.
            id (any): ID.

        Returns:
            cursor (DictCursor): Cursor.
        """
        return self.get(
            column=column,
            key=Identifier("id"),
            key_value=id
        )

    def get(
            self,
            column: Identifier,
            key: Identifier,
            key_value: any
    ) -> DictCursor:
        """
        Gets the value of a column from the database.

        Args:
            column (Identifier): Column name.
            key (Identifier): Key column name.
            key_value (any): Key column value.

        Returns:
            cursor (DictCursor): Cursor.
        """
        cursor: DictCursor = self.connection.cursor()
        cursor.execute(
            SQL(
                r"SELECT {column} FROM {table} WHERE {key} = %s;"
            ).format(
                column=column,
                table=self._table_name,
                key=key
            ),
            (key_value,)
        )

        return cursor

    def id_set(
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
        self.set(
            column=column,
            value=value,
            key=Identifier("id"),
            key_value=id
        )

    def set(
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
        with self.connection.cursor() as cursor:
            cursor.execute(
                SQL(
                    r"UPDATE {table} SET {column} = %s WHERE {key} = %s;".format(
                        column=column,
                        table=self._table_name,
                        key=key
                    )
                ),
                (value, key_value)
            )
