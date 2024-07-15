"""
Contains database connection information and shared handlers.
"""
# Standard Library Imports

# Third Party Imports

# Local Imports
from ..internals.config import Config
from .handlers import *

# Constants
__all__ = ["database"]


class Database:
    """
    Database connection pool.
    """
    def __init__(self, config: Config) -> None:
        self.config = config
        self.pool = None