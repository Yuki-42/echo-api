"""
Contains the user routes.
"""
from typing import Annotated
from uuid import UUID

# Third Party Imports
from fastapi import APIRouter, Depends, WebSocket
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from pydantic import BaseModel

# Local Imports
from ..config.config import CONFIG
from ..db.database import Database
from ..db.types.user import User
from ..models.secure import PrivateUser as PrivateUserModel
from ..models.user import User as UserModel

# Standard Library Imports

# Constants
__all__ = [
    "users_router"
]

from ..ws_workers.users_worker import UsersWorker

# Create API router
users_router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"]
)


class CreateUserData(BaseModel):
    """
    Create user data model.
    """
    username: str
    email: str
    password: str


class LoginUserData(BaseModel):
    """
    Login user data model.
    """
    email: str
    password: str


@users_router.websocket("/")
async def users_ws(
        websocket: WebSocket,
        database: Annotated[Database, Depends(Database.new)]
) -> None:
    """
    Route to establish a users websocket.
    """
    await websocket.accept()

    # Pass off to the worker
    worker: UsersWorker = UsersWorker(websocket, database)
    await worker.run()


@users_router.post("/<verification_code>", tags=["users"])
async def verify_user(
        verification_code: str,
        database: Annotated[Database, Depends(Database.new)]
):
    """
    Verifies a user's email address.
    """
    # Get user
    user: VerificationCode = await database.secure.get_verification_code(verification_code)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the validation code is expired



    await user.set_is_verified(True)

    # Return user

# @users_router.post("/login", tags=["users"])
# async def login_user(
#         data: CreateUserData,
#         request: Request
# ) -> PyJWT:
#     """
#     Creates a new auth token for the user.
#     """
#     # Get database connection
#     db: Database = request.state.db
#
#     # Check if the user exists
#     user: User = await db.users.email_get(data.email)
#
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     # Get hashed password
#     password: Password = await db.secure.get_password(user.id)
#
#     # Check password
#     if not db.secure.verify_password(data.password, password.hash):
#         raise HTTPException(status_code=403, detail="Incorrect password")
#
#     # Build a new access token
#     token: Token = await db.secure.new_token(user.id)
#
#     # Encode token
#     return token.encode()
#
