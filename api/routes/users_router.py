# Standard Library Imports

# Third Party Imports
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

# Local Imports

# Constants
__all__ = ["users_router"]

# Create API router
users_router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"]
)


@users_router.get("/", tags=["users"])
async def read_users() -> dict:
    return {
        "message": "Welcome to the disbroad API. Use /docs to view the API documentation."
    }
