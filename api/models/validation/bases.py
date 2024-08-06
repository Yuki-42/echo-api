"""
Contains the base models used for WS validation.
"""

# Standard Library Imports

# Third Party Imports
from pydantic import BaseModel

# Local Imports

# Constants
__all__ = [
    "BaseMessage",
    "BaseError",
]


class BaseMessage(BaseModel):
    """
    Base message model.
    """
    action: str


class BaseError(BaseMessage):
    """
    Base error model.
    """
    error: str
