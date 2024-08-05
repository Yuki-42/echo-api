"""
Contains the user routes.
"""
from typing import Annotated

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


@users_router.post(
    "/", tags=["users"], responses={
        409: {"description": "User already exists"},
        430: {"description": "Password does not meet requirements"}
    }
)
async def create_user(
        data: CreateUserData,
        request: Request,
        database: Annotated[Database, Depends(Database.new)]
) -> PrivateUserModel:
    """
    Creates a new user.
    """
    # Do user password checks before anything else to minimise in-flight time for password
    if len(data.password) > CONFIG.user_security.password_maximum_length:

        raise HTTPException(status_code=430, detail="Password too long")

    if len(data.password) < CONFIG.user_security.password_minimum_length:
        raise HTTPException(status_code=430, detail="Password too short")

    # Count numbers of each character type
    uppercase: int = 0
    lowercase: int = 0
    number: int = 0
    special: int = 0

    for char in data.password:
        if char.isupper():
            uppercase += 1
        elif char.islower():
            lowercase += 1
        elif char.isdigit():
            number += 1
        else:
            special += 1

    if uppercase < CONFIG.user_security.password_require_uppercase:
        raise HTTPException(status_code=430, detail=f"Password requires {CONFIG.user_security.password_require_uppercase} uppercase characters")

    if lowercase < CONFIG.user_security.password_require_lowercase:
        raise HTTPException(status_code=430, detail=f"Password requires {CONFIG.user_security.password_require_lowercase} lowercase characters")

    if number < CONFIG.user_security.password_require_number:
        raise HTTPException(status_code=430, detail=f"Password requires {CONFIG.user_security.password_require_number} number characters")

    if special < CONFIG.user_security.password_require_special_character:
        raise HTTPException(status_code=430, detail=f"Password requires {CONFIG.user_security.password_require_special_character} special characters")

    # Get database connection
    db: Database = request.state.db

    # Check if the user exists
    user: User = await db.users.email_get(data.email)

    if user is not None:
        raise HTTPException(status_code=409, detail="User already exists")

    # Create user
    user = await db.users.new(data.email, data.username, data.password)

    # Close database connection
    await database.close()

    return await user.to_private()


@users_router.put("/", tags=["users"])
async def update_user(
        data: CreateUserData,
        request: Request,
        database: Annotated[Database, Depends(Database.new)]
) -> UserModel:
    """
    Updates a user.
    """

    # Check if the user exists
    user: User = await database.users.email_get(data.email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user
    user = await database.users.update(user.id, data.email, data.username, data.password)

    return await user.to_public()

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
