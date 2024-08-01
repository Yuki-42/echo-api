"""
Contains the user routes.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from pydantic import BaseModel

# Local Imports
from ..db.database import Database
from ..db.types.user import User
from ..models.user import User as UserModel
from ..models.private import PrivateUser as PrivateUserModel

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


@users_router.post("/", tags=["users"], responses={409: {"description": "User already exists"}})
async def create_user(
        data: CreateUserData,
        request: Request
) -> PrivateUserModel:
    """
    Creates a new user.
    """
    # Get database connection
    db: Database = request.state.db

    # Check if the user exists
    user: User = await db.users.email_get(data.email)

    if user is not None:
        raise HTTPException(status_code=409, detail="User already exists")

    # Create user
    user = await db.users.new(data.email, data.username, data.password)

    return await user.to_private()


@users_router.post("/login", tags=["users"])
async def login_user(
        data: CreateUserData,
        request: Request
) -> PrivateUserModel:
    """
    Logs in a user.
    """
    # Get database connection
    db: Database = request.state.db

    # Check if the user exists
    user: User = await db.users.email_get(data.email)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check password
    if not db.secure.verify_password(data.password, data.password):
        raise HTTPException(status_code=403, detail="Incorrect password")

    return await user.to_private()
