"""
Contains the base worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

# Local Imports

# Constants
__all__ = [
    "BaseWorker",
]


class BaseWorker:
    """
    Base worker class.
    """
    connection: WebSocket

    def __init__(
            self,
            connection: WebSocket
    ) -> None:
        """
        Initialise the worker.
        """
        self.connection = connection
