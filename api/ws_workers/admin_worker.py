"""
Contains the WS Admin Worker.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import WebSocket

# Local Imports

# Constants
__all__ = [
    "AdminWorker"
]


class AdminWorker:
    """
    Worker to handle admin WebSocket connections.
    """
    connection: WebSocket

    def __init__(
            self,
            connection: WebSocket
    ) -> None:
        """
        Initialise the worker.

        Args:
            connection (WebSocket): WebSocket connection.
        """
        self.connection = connection

        # Begin the processor loop
        self.processor()

    async def processor(self) -> None:
        """
        Processor loop.
        """
        while True:
            data: dict = await self.connection.receive_json()

            # Ensure that the base level spec is present
            if "action" not in data:
                await self.connection.send_json(
                    {"error": "No action provided."}
                )
                continue

            # Match action
            action: str = data.get("action")

            match action:
                case "get_users":
                    await self.connection.send_json(
                        {"action": "pong"}
                    )
                case "delete_user":
                    await self.connection.close()
                    break
                case _:
                    await self.connection.send_json(
                        {"error": "Invalid action."}
                    )
