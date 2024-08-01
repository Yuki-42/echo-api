"""
Contains the base handler.
"""

# Standard Library Imports

# Third Party Imports
from psycopg import AsyncConnection

# Local Imports
from ..base_db_interactor import BaseDbInteractor

# Constants
__all__ = ["BaseHandler"]


class BaseHandler(BaseDbInteractor):
    """
    Base handler.
    """

    def close(self) -> None:
        """
        Close connection.
        """
        self.connection.close()
        self.connection = None
