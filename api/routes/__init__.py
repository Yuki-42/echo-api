"""
Init file for routes
"""
from .api_router import api_router
from .users_router import users_router

__all__ = [
    "api_router",
    "users_router"
]
