"""
Main file for API.
"""
# Standard Library Imports
from sys import platform
from typing import Callable

# Third Party Imports
from fastapi import APIRouter, FastAPI
from fastapi.security import OAuth2PasswordBearer

# Local Imports
from .routes import *

# Constants
__all__ = [
    "app",
    "create_app",
]

# Set event loop policy for Windows
if platform == "win32":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy  # These imports are here because they don't exist on windows

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
