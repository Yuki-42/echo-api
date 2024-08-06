"""
Contains models used for validation of data in the users WS.
"""
from uuid import UUID

# Standard Library Imports

# Third Party Imports
from pydantic import BaseModel

# Local Imports
from .bases import BaseMessage, BaseError

# Constants
__all__ = [

]


class RegisterInputData(BaseModel):
    """
    Model for registering a user.
    """
    username: str
    email: str
    password: str


class RegisterInput(BaseMessage):
    """
    Model for registering a user.
    """
    data: RegisterInputData


class LoginInputData(BaseModel):
    """
    Model for logging in a user.
    """
    email: str
    password: str


class LoginInput(BaseMessage):
    """
    Model for logging in a user.
    """
    data: LoginInputData
