"""
Contains the WS Users Worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

# Local Imports
from .base_worker import BaseWorker
from ..db import Database

# Constants
__all__ = [
    "UsersWorker"
]


class UsersWorker(BaseWorker):
    """
    Worker to handle user WebSocket connections.
    """

    def __init__(
            self,
            connection: WebSocket,
            database: Database
    ) -> None:
        """
        Initialise the worker.
        """
        super().__init__(connection)

    async def run(self) -> None:
        """
        Run the worker.
        """
        while True:
            try:
                data: dict = await self.connection.receive_json()
            except WebSocketDisconnect:
                await self.connection.close()
                return
