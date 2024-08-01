"""
Contains private models that can only be accessed by the user they are owned by.
"""

# Standard Library Imports
from datetime import datetime

# Third Party Imports
from pydantic import BaseModel

# Local Imports
from .user import User
from .secure import Token, Password

# Constants
__all__ = [
    "PrivateUser"
]


class PrivateUser(User):
    """
    Private user model.
    """
    tokens: list[Token]
    password: Password
