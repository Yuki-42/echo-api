"""
Contains the security scheme and crypt config for the API.
"""

# Standard Library Imports
from datetime import datetime, timedelta
from warnings import warn

# Third Party Imports
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWT, decode, encode
from passlib.context import CryptContext
from rsa import PrivateKey, PublicKey, newkeys

# Local Imports
from ..config.config import CONFIG

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
        expires_delta: int = CONFIG.auth.key_expires
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
        CONFIG.auth.secret_key,
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
        CONFIG.auth.secret_key,
        algorithms=["HS256"]
    )


def generate_keypair() -> tuple[PublicKey, PrivateKey]:
    """
    Generates a public and private keypair for use with the API.

    Returns:
        tuple[str, str]: The public and private keypair.
    """
    if CONFIG.auth.key_size < 2048:
        warn("Key size is less than 2048 bits, which is not recommended for security.")

    return newkeys(CONFIG.auth.key_size)
