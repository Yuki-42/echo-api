"""
Init file for routes
"""
# Standard Library Imports

# Third Party Imports

# Local Imports
from .admin_router import administrator_router
from .api_router import api_router
from .users_router import users_router

# Constants
__all__ = [
    "api_router",
    "users_router",
    "administrator_router",
]
