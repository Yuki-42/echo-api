"""
Main file for API.
"""
# Standard Library Imports
from asyncio import get_event_loop, get_running_loop
from typing import Callable

# Third Party Imports
from fastapi import APIRouter, FastAPI
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer

# Local Imports
from .db.database import Database
from .internals.config import Config
from .routes import *


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

