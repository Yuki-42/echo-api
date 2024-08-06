"""
Contains all security related models
"""

# Standard Library Imports
from datetime import datetime

# Third Party Imports
from pydantic import BaseModel

# Local Imports
from .base import BaseTableModel
from .user import User

# Constants
__all__ = [
    "Token",
    "Password",
]


class VerificationCode(BaseTableModel):
    """
    Verification code model.
    """
    user: User
    code: str
    expires: datetime


class Token(BaseTableModel):
    """
    Token model.
    """
    user: User
    token: str
    last_used: datetime


class Password(BaseTableModel):
    """
    Password model.
    """
    hash: str
    last_updated: datetime


class PrivateUser(BaseModel):
    """
    Private user model.
    """
    tokens: list[Token]
