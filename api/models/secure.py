"""
Contains all security related models
"""
# Standard Library Imports
from datetime import datetime
from uuid import UUID

# Third Party Imports
from pydantic import BaseModel

# Local Imports
from . import User

# Constants
__all__ = [
    "Device",
    "Token"
]


class Device(BaseModel):
    """
    Device model.
    """
    id: UUID
    created_at: datetime
    name: str
    ip: str
    mac: str
    lang: str
    os: str
    screen_size: str
    country: str


class Token(BaseModel):
    """
    Token model.
    """
    user: User
    device: Device
    token: str
    last_used: datetime
