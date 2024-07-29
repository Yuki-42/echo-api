"""
User Model.
"""
# Standard Library Imports
from typing import Optional, Annotated
from enum import Enum
from uuid import UUID
from datetime import datetime

# Third Party Imports
from pydantic import BaseModel

# Local Imports

# Constants

__all__ = [
    "User",
    "StatusType",
    "Status",
    "File",
    "Device",
    "Token",
    "PrivateUser"
]


class StatusType(int, Enum):
    online = 0
    offline = 1
    away = 2
    dnd = 3
    playing = 4
    watching = 5
    listening = 6


class Status(BaseModel):
    """
    Status model.
    """
    type: StatusType
    message: Optional[str]


class User(BaseModel):
    """
    User model.
    """
    id: UUID
    created_at: datetime
    email: str
    username: str
    icon: UUID
    bio: Optional[str]
    status: Status
    last_online: datetime
    is_online: bool
    is_banned: bool
    is_verified: bool


class File(BaseModel):
    """
    File model.
    """
    id: UUID
    created_at: datetime
    created_by: User


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


class PrivateUser(User):
    """
    Private user model.
    """
    tokens: list[Token]
    password_last_updated: datetime
