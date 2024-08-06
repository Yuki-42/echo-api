"""
Base API router.
"""

# Standard Library Imports

# Third Party Imports
from fastapi import APIRouter, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

# Local Imports

# Constants
__all__ = [
    "api_router"
]
SWAGGER_DARK_CSS: str = "https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css"

# Create API router
api_router: APIRouter = APIRouter()


# Create routes
@api_router.get("/", tags=["root"])
async def read_root() -> dict:
    """
    Root route of the API.
    """
    return {"message": "Welcome to the disbroad API. Use /docs to view the API documentation."}


@api_router.get("/docs", include_in_schema=False)
async def docs(request: Request) -> HTMLResponse:
    """
    Route to display the API documentation
    """
    return get_swagger_ui_html(
        openapi_url=request.app.openapi_url,
        title="Disbroad API",
        swagger_css_url=SWAGGER_DARK_CSS
    )


@api_router.get("/openapi.json", include_in_schema=False)
async def openapi(request: Request) -> dict:
    """
    Route to display the OpenAPI schema
    """
    return request.app.openapi()


@api_router.get("/teapot", include_in_schema=False)
async def teapot() -> dict:
    """
    Teapot route.
    """
    raise HTTPException(status_code=418, detail="I'm a teapot.")
