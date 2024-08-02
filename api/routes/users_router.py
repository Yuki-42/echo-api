"""
Contains the user routes.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from jwt import PyJWT
from pydantic import BaseModel

# Local Imports
from ..config.config import CONFIG
from ..db.database import Database
from ..db.types.user import User
from ..models.private import PrivateUser as PrivateUserModel
from ..models.secure import Password, Token
from ..models.user import User as UserModel

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


@users_router.get("/<string: user_id>", tags=["users"])
async def read_users(
        user_id: str,
        request: Request
) -> UserModel | PrivateUserModel:
    """
    Gets a user by ID.
    """
    # Get database connection
    db: Database = request.state.db

    # Check if user exists
    user: User = await db.users.id_get(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await user.to_public()


@users_router.post(
    "/", tags=["users"], responses={
        409: {"description": "User already exists"},
        430: {"description": "Password does not meet requirements"}
    }
    )
async def create_user(
        data: CreateUserData,
        request: Request
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

    return await user.to_private()


@users_router.put("/", tags=["users"])
async def update_user(
        data: CreateUserData,
        request: Request
) -> UserModel:
    """
    Updates a user.
    """
    # Get database connection
    db: Database = request.state.db

    # Check if the user exists
    user: User = await db.users.email_get(data.email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user
    user = await db.users.update(user.id, data.email, data.username, data.password)

    return await user.to_public()


@users_router.delete("/", tags=["users"])
async def delete_user(
        data: CreateUserData,
        request: Request
) -> UserModel:
    """
    Deletes a user.
    """
    # Get database connection
    db: Database = request.state.db

    # Check the signature included in the request

    # Check if the user exists
    user: User = await db.users.email_get(data.email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete user
    user = await db.users.delete(user.id)

    return await user.to_public()


@users_router.post("/login", tags=["users"])
async def login_user(
        data: CreateUserData,
        request: Request
) -> PyJWT:
    """
    Creates a new auth token for the user.
    """
    # Get database connection
    db: Database = request.state.db

    # Check if the user exists
    user: User = await db.users.email_get(data.email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Get hashed password
    password: Password = await db.secure.get_password(user.id)

    # Check password
    if not db.secure.verify_password(data.password, password.hash):
        raise HTTPException(status_code=403, detail="Incorrect password")

    # Build a new access token
    token: Token = await db.secure.new_token(user.id)

    # Encode token
    return token.encode()
