"""
Common methods imported by routes as dependencies.

See https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
"""

# Standard Library Imports

# Third Party Imports

# Local Imports
from .config import CONFIG
from .db import Database

# Constants
__all__ = [
    "get_database"
]


async def get_database() -> Database:
    """
    Get database connection.

    Returns:
        Database: Database connection.
    """
    return await Database.new(CONFIG)

