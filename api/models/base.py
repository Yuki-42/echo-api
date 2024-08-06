"""
Contains the base model that all top level table models inherit from.
"""

# Standard Library Imports
from uuid import UUID
from datetime import datetime

# Third Party Imports
from pydantic import BaseModel

# Local Imports

# Constants
__all__ = [
    "BaseTableModel",
]


class BaseTableModel(BaseModel):
    """
    Base table model.
    """
    id: UUID
    created_at: datetime
