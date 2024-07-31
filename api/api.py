"""
Main file for API.
"""
# Standard Library Imports
from typing import Callable

# Third Party Imports
from fastapi import APIRouter, FastAPI
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer

from .db.database import Database
from .internals.config import Config
# Local Imports
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

    # Create required services
    config: Config = Config()
    database: Database = Database(config)

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

    @api.middleware("http")
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
        request.state.db = database
        response = await call_next(request)
        return response

    @api.on_event("shutdown")
    async def shutdown_event() -> None:
        """
        Shutdown event.
        """
        await database.close()

    # Set token url
    ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

    return api


app: FastAPI = create_app()
