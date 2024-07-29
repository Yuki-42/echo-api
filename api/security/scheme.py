"""
Contains the security scheme and crypt config for the API.
"""

# Standard Library Imports

# Third Party Imports
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Local Imports
from ..internals.config import Config

# Constants
__all__ = [
    "oauth2_scheme",
    "crypt_context"
]

# Create security scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


# Create crypt config
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")