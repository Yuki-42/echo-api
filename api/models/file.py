"""
Contains file related models.
"""

# Standard Library Imports
from datetime import datetime
from uuid import UUID

# Third Party Imports
from pydantic import BaseModel

# Local Imports

# Constants
__all__ = [
    "File",
]


class File(BaseModel):
    """
    File model.
    """
    id: UUID
    created_at: datetime
    created_by: UUID
