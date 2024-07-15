"""
Main file for API.
"""
from typing import Callable

# Standard Library Imports

# Third Party Imports
from fastapi import FastAPI
from fastapi.requests import Request

# Local Imports
from .routes import *
from .internals.config import Config
from .db.database import Database


def create_app() -> FastAPI:
    """
    Create FastAPI instance.
    """
    # Create FastAPI instance
    app: FastAPI = FastAPI()

    # Create required services
    config: Config = Config()
    database: Database = Database(config)

    # Register routes
    app.include_router(api_router)
    app.include_router(users_router)

    @app.middleware("http")
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

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        """
        Shutdown event.
        """
        await database.close()

    return app


app: FastAPI = create_app()
