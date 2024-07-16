# Standard Library Imports

# Third Party Imports
from fastapi import APIRouter
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
    user: User = db.users.get(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user.to_model()


@users_router.post("/", tags=["users"])
async def create_user(
        username: str,
        email: str,
        password: str,
        request: Request
) -> PrivateUserModel:
    """
    Creates a new user.
    """
    # Get database connection
    db: Database = request.state.db

    # Check if the user exists already

