"""
Contains the base database interactor.
"""

# Standard Library Imports

# Third Party Imports
from psycopg import AsyncConnection

# Local Imports

# Constants
__all__ = [
    "BaseDbInteractor",
]


class BaseDbInteractor:
    """
    Base database interaction class. Implements the connection and handlers properties.
    """
    connection: AsyncConnection

    def __init__(
            self,
            connection: AsyncConnection
    ) -> None:
        """
        Initialize BaseDbInteractor.

        Args:
            connection (AsyncConnection): Database connection.
        """
        self.connection = connection

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.__dict__}>"

    @property
    def users(self):  # This is a great example of how to use a property to create a handler. (I think)
        """
        Get users handler.
        """
        from .handlers.user_handler import UsersHandler
        return UsersHandler(self.connection)

    @property
    def secure(self):
        """
        Get secure handler.
        """
        from .handlers.secure_handler import SecureHandler
        return SecureHandler(self.connection)

    @property
    def files(self):
        """
        Get files handler.
        """
        from .handlers.file_handler import FilesHandler
        return FilesHandler(self.connection)
