"""
Contains file related models.
"""

# Standard Library Imports
from datetime import datetime
from uuid import UUID

# Third Party Imports
from pydantic import BaseModel

# Local Imports
from .base import BaseTableModel

# Constants
__all__ = [
    "File",
]


class File(BaseTableModel):
    """
    File model.
    """
    created_by: UUID
