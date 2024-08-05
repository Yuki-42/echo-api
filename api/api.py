"""
Main file for API.
"""
# Standard Library Imports
from sys import platform
from typing import Callable

# Third Party Imports
from fastapi import APIRouter, FastAPI, WebSocket, Response, Request
from fastapi.security import OAuth2PasswordBearer
from psycopg_pool import AsyncConnectionPool

# Local Imports
from .db.database import Database
from .config import CONFIG
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


# Superclass FastAPI to include a state
class StatefulAPI(FastAPI):
    """
    Superclass to provide state storage (just a dict)
    """
    state: dict[str, any]


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


@app.on_event("startup")
async def startup_event() -> None:
    """
    Startup event.
    """
    # Create the connection pool
    connection_pool: AsyncConnectionPool = AsyncConnectionPool(  # This is broken
        conninfo=f"dbname={CONFIG.db.name} user={CONFIG.db.user} password={CONFIG.db.password} host={CONFIG.db.host} port={CONFIG.db.port}",
        open=False,
        min_size=4,
        max_size=10,
        timeout=10,
    )
    await connection_pool.open()

    app.state.pool = connection_pool


@app.middleware("http")
async def db_middleware(
        request: Request,
        call_next: callable
) -> Response:
    """
    Middleware to connect to the database.
    """
    with app.state.pool.connection() as connection:
        request.state.db = await Database.new(connection)
        response = await call_next(request)
        await request.state.db.close()
        return response
