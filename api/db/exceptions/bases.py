"""
Contains the base error classes.
"""

# Standard Library Imports
from typing import Any
from uuid import UUID

# Third Party Imports

# Local Imports

# Constants
__all__ = [
    "DatabaseException"
]


class DatabaseException(Exception):
    """
    Base exception for database errors.
    """
    table: str
    identifier: str | int | UUID

    def __init__(
            self,
            table: str,
            identifier: str | int | UUID
    ) -> None:
        """
        Initialise the exception.
        """
        self.table = table
        self.identifier = identifier
        super().__init__(
            f"Error in {table} with key {identifier}."
        )
