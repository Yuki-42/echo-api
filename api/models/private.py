"""
Contains private models that can only be accessed by the user they are owned by.
"""

# Standard Library Imports

# Third Party Imports

# Local Imports
from .user import User
from .secure import Token

# Constants
__all__ = [
    "PrivateUser"
]


class PrivateUser(User):
    """
    Private user model.
    """
    tokens: list[Token]
    password: str
