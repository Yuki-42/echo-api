"""
Main file for API.
"""
# Standard Library Imports
from sys import platform
from typing import Callable
from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy

# Third Party Imports
from fastapi import APIRouter, FastAPI, WebSocket
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer

# Local Imports
from .db.database import Database
from .config.config import Config
from .routes import *

# Constants
__all__ = [
    "app",
    "create_app",
]

# Set event loop policy for Windows
if platform == "win32":
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())


def create_app(
        extensions: list[APIRouter] = None,
        middleware: list[Callable] = None
) -> FastAPI:
    """
    Create FastAPI instance.
    """
    # Create FastAPI instance
    api: FastAPI = FastAPI()

    # Register routes
    api.include_router(api_router)
    api.include_router(users_router)
    api.include_router(administrator_router)

    # Register extensions
    if extensions:
        for extension in extensions:
            api.include_router(extension)

    # Register middleware
    if middleware:
        for middleware_item in middleware:
            api.add_middleware(middleware_item)

    # Set token url
    ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

    return api


# Create app
app: FastAPI = create_app()


# Add middleware for db on both HTTP and WebSocket
@app.middleware("http")
async def db_session_middleware(
        request: Request,
        call_next: Callable
) -> None:
    """
    Middleware to add database connection to request state.

    Args:
        request (Request): Request object.
        call_next (Callable): Next function to call.
    """
    # Create required services
    config: Config = Config()
    database: Database = await Database.new(config)

    request.state.db = database
    response = await call_next(request)
    return response


@app.middleware("ws")
async def db_session_middleware(
        websocket: WebSocket,
        call_next: Callable
) -> None:
    """
    Middleware to add database connection to request state.

    Args:
        websocket (WebSocket): WebSocket object.
        call_next (Callable): Next function to call.
    """
    # Create required services
    config: Config = Config()
    database: Database = await Database.new(config)

    websocket.state.db = database
    response = await call_next(websocket)
    return response

