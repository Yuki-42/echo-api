"""
Base DB type.
"""

# Standard Library Imports
from typing import TypeVar, Type

# Third Party Imports
from psycopg2.extras import DictConnection

# Local Imports

# Constants
__all__ = ["BaseType"]

from pydantic import BaseModel


class BaseType:
    """
    Base DB type.

    Provides the connection attribute.
    """

    _connection: DictConnection

    def __init__(
            self
    ) -> None:
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
