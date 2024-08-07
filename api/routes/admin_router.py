"""
Administrator WS API Router
"""
# Standard Library Imports
from hashlib import md5
from secrets import token_bytes
from typing import Annotated

# Third Party Imports
from fastapi import APIRouter, WebSocket, Depends
from rsa import encrypt
from starlette.websockets import WebSocketDisconnect

# Local Imports
from ..db import Database
from ..config import CONFIG
from ..ws_workers import AdminWorker

# Constants
__all__ = [
    "administrator_router"
]

# Create API router
administrator_router: APIRouter = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


# Create WS connection route
@administrator_router.websocket("/")
async def admin_ws(
        websocket: WebSocket,
        database: Annotated[Database, Depends(Database.new)]
) -> None:
    """
    Route to establish a WebSocket connection for the administrator.
    """
    await websocket.accept()

    # Generate a token for the connection
    token: bytes = token_bytes(32)

    # Encrypt the token using the public key
    encrypted_token: bytes = encrypt(token, CONFIG.server.owner_public_key)

    # Send the token to the client
    await websocket.send_bytes(encrypted_token)

    # Calculate the expected token
    client_expected: bytes = md5(token).digest()

    # Receive the token back from the client
    try:
        client_actual: bytes = await websocket.receive_bytes()  # This is causing an error
    except WebSocketDisconnect:
        return  # Gracefully handle disconnect

    # Check if the response is exactly what was expected
    if client_actual != client_expected:
        await websocket.send_json({"message": "Authentication failed."})
        await websocket.close()
        return

    # Send the client a message to say that they are authenticated
    await websocket.send_json(
        {"message": "Authenticated."}
    )

    # We now know that the user is authenticated for this session we will accept the event loop and hand it off to the processor
    worker: AdminWorker = AdminWorker(
        websocket,
        database
    )
    await worker.run()
