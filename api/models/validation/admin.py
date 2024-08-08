"""
Contains models used for validation of data in the admin WS.
"""
from typing import Optional

# Standard Library Imports

# Third Party Imports
from pydantic import BaseModel

# Local Imports
from .bases import BaseMessage
from ..user import User

# Constants
__all__ = [
    "GetUsersInputData",
    "GetUsersInput",
    "DeleteUserInputData",
    "DeleteUserInput",
]


class GetUsersInputData(BaseModel):
    """
    Model for getting users.
    """
    page: int
    page_size: int


class GetUsersInput(BaseMessage):
    """
    Model for getting users.
    """
    data: GetUsersInputData


class DeleteUserInputData(BaseModel):
    """
    Model for deleting a user.
    """
    id: str


class DeleteUserInput(BaseMessage):
    """
    Model for deleting a user.
    """
    data: DeleteUserInputData
