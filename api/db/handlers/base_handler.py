"""
Contains the base handler.
"""

# Standard Library Imports

# Third Party Imports
from psycopg2.extras import DictConnection

# Local Imports

# Constants
__all__ = ["BaseHandler"]


class BaseHandler:
    """
    Base handler.
    """
    _connection: DictConnection

    def __init__(
            self,
            connection: DictConnection
    ) -> None:
        """
        Initialize BaseHandler.

        Args:
            connection (DictConnection): Database connection.
        """
        self._connection = connection

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    @property
    def connection(self) -> DictConnection:
        """
        Get connection.

        Returns:
            DictConnection: Database connection.
        """

        if not self._connection:
            raise AttributeError("Connection not set.")

        return self._connection

    def close(self) -> None:
        """
        Close connection.
        """
        self._connection.close()
        self._connection = None

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
