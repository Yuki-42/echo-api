"""
Contains all security related models
"""

# Standard Library Imports
from datetime import datetime
from uuid import UUID

# Third Party Imports
from pydantic import BaseModel

# Local Imports
from .user import User

# Constants
__all__ = [
    "Token",
    "Password",
]


class Token(BaseModel):
    """
    Token model.
    """
    user: User
    token: str
    last_used: datetime


class Password(BaseModel):
    """
    Password model.
    """
    hash: str
    last_updated: datetime


class PrivateUser(User):
    """
    Private user model.
    """
    tokens: list[Token]
