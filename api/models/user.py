"""
Contains user related models.
"""

# Standard Library Imports
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID

# Third Party Imports
from pydantic import BaseModel

# Local Imports
from .base import BaseTableModel

# Constants

__all__ = [
    "User",
    "StatusType",
    "Status",
]

from pydantic.main import IncEx


class StatusType(int, Enum):
    offline: int = 0
    online: int = 1
    away: int = 2
    dnd: int = 3
    playing: int = 4
    watching: int = 5
    listening: int = 6


class Status(BaseModel):
    """
    Status model.
    """
    type: StatusType
    text: str


class User(BaseTableModel):
    """
    User model.
    """
    email: str
    username: str
    icon: Optional[UUID] = None
    bio: Optional[str] = None
    status: Status
    last_online: datetime
    is_online: bool
    is_banned: bool
    is_verified: bool

