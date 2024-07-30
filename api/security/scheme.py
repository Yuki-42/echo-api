"""
Contains the security scheme and crypt config for the API.
"""

# Standard Library Imports
from datetime import timedelta
from datetime import datetime

# Third Party Imports
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jwt import encode, decode, PyJWT

# Local Imports
from ..internals.config import CONFIG

# Constants
__all__ = [
    "oauth2_scheme",
    "crypt_context"
]

# Create security scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Create crypt config
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encode_access_token(
        data: dict[str, any],
        expires_delta: int = CONFIG.auth.keyExpires
) -> PyJWT:
    """
    Encodes the provided data into a JWT token.

    Args:
        data (dict[str, any]): The data to encode.
        expires_delta (int): The time in seconds for the token to expire.

    Returns:
        PyJWT: The encoded token.
    """
    to_encode: dict[str, any] = data.copy()  # Copy the data to prevent modification, as the data is mutable.
    to_encode.update(
        {
            "exp": datetime.now() + timedelta(seconds=expires_delta)
        }
    )
    return encode(
        to_encode,
        CONFIG.auth.secretKey,
        algorithm="HS256"
    )


def decode_access_token(
        token: str
) -> dict[str, any]:
    """
    Decodes the provided token into a dictionary.

    Args:
        token (str): The token to decode.

    Returns:
        dict[str, any]: The decoded token.
    """
    return decode(
        token,
        CONFIG.auth.secretKey,
        algorithms=["HS256"]
    )
