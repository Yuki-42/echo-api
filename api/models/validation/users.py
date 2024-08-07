"""
Contains models used for validation of data in the users WS.
"""

# Standard Library Imports

# Third Party Imports
from pydantic import BaseModel

# Local Imports
from .bases import BaseMessage
from ..user import User

# Constants
__all__ = [
    "RegisterInputData",
    "RegisterInput",
    "RegisterOutputData",
    "LoginInputData",
    "LoginInput",
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


class RegisterOutputData(BaseModel):
    """
    Model for registering a user.
    """
    user: User


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
