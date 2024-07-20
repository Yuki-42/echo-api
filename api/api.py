"""
Main file for API.
"""
# Standard Library Imports
from typing import Callable

# Third Party Imports
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer

# Local Imports
from .routes import *
from .internals.config import Config
from .db.database import Database


def create_app() -> FastAPI:
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

    @api.middleware("http")
    async def db_session_middleware(request: Request, call_next: Callable) -> None:
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
