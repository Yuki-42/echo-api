"""
Contains the base handler.
"""

# Standard Library Imports

# Third Party Imports

# Local Imports
from ..base_db_interactor import BaseDbInteractor

# Constants
__all__ = [
    "BaseHandler",
]


class BaseHandler(BaseDbInteractor):
    """
    Base handler.
    """

    async def close(self) -> None:
        """
        Close connection.
        """
        await self.connection.close()
