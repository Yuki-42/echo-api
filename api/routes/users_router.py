# Standard Library Imports
from typing import Annotated

# Third Party Imports
from fastapi import APIRouter, Form, Body
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

# Local Imports
from ..db.database import Database
from ..db.types.user import User
from ..models.user import User as UserModel, PrivateUser as PrivateUserModel

# Constants
__all__ = ["users_router"]

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
    user: User = db.users.id_get(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user.to_public()


@users_router.post("/", tags=["users"])
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
    user: User = db.users.email_get(data.email)

    if user is not None:
        raise HTTPException(status_code=409, detail="User already exists")

    # Create user
    user = db.users.new(data.email, data.username, data.password)

    return user.to_private()



