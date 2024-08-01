"""
Contains the base handler.
"""

# Standard Library Imports

# Third Party Imports
from psycopg import AsyncConnection

# Local Imports

# Constants
__all__ = ["BaseHandler"]


class BaseHandler:
    """
    Base handler.
    """
    connection: AsyncConnection

    def __init__(
            self,
            connection: AsyncConnection
    ) -> None:
        """
        Initialize BaseHandler.

        Args:
            connection (AsyncConnection): Database connection.
        """
        self.connection = connection

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def close(self) -> None:
        """
        Close connection.
        """
        self.connection.close()
        self.connection = None

    @property
    def users(self):  # This is a great example of how to use a property to create a handler. (I think)
        """
        Get users handler.
        """
        from .user_handler import UsersHandler
        return UsersHandler(self.connection)

    @property
    def secure(self):
        """
        Get secure handler.
        """
        from .secure_handler import SecureHandler
        return SecureHandler(self.connection)
