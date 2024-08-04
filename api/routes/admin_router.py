"""
Administrator WS API Router
"""
# Standard Library Imports
from hashlib import md5
from secrets import token_bytes

# Third Party Imports
from fastapi import APIRouter, WebSocket
from rsa import encrypt

# Local Imports
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
@administrator_router.websocket("/ws")
async def admin_ws(
        websocket: WebSocket
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
    client_actual: bytes = await websocket.receive_bytes()  # This is causing an error

    # Check if the response is exactly what was expected
    if client_actual != client_expected:
        await websocket.close()
        return

    # Send the client a message to say that they are authenticated
    await websocket.send_json(
        {"message": "Authenticated."}
    )

    # We now know that the user is authenticated for this session we will accept the event loop and hand it off to the processor
    worker: AdminWorker = AdminWorker(
        websocket,
        websocket.state.db
    )
    await worker.run()
