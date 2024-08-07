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
    "GetUsersInput"
]


class GetUsersInputData(BaseMessage):
    """
    Model for getting users.
    """
    page: int
    page_size: int


class GetUsersInput(BaseModel):
    """
    Model for getting users.
    """
    data: GetUsersInputData
