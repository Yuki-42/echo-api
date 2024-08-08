"""
Contains user related database exceptions.
"""
from typing import Any
from uuid import UUID

# Standard Library Imports

# Third Party Imports

# Local Imports
from .bases import DatabaseException

# Constants
__all__ = [
    "UserDoesNotExist",
    "UserAlreadyExists",
]


class UserDoesNotExist(DatabaseException):
    """
    Exception for when a user does not exist.
    """

    def __init__(
            self,
            identifier: str | int | UUID
    ) -> None:
        """
        Initialise the exception.
        """
        super().__init__("users", identifier)
        self.message = f"User with ID {identifier} does not exist."


class UserAlreadyExists(DatabaseException):
    """
    Exception for when a user already exists.
    """
    def __init__(
            self,
            identifier: str | int | UUID
    ) -> None:
        """
        Initialise the exception.
        """
        super().__init__("users", identifier)
        self.message = f"User with ID {identifier} already exists."

