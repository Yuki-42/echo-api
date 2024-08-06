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

# Constants
__all__ = [
    "oauth2_scheme",
    "crypt_context"
]

# Create security scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Create crypt config
crypt_context = CryptContext(schemes=["argon2"], deprecated="auto")


def encode_access_token(
        data: dict[str, any],
        expires_delta: int,
        secret_key: str
) -> PyJWT:
    """
    Encodes the provided data into a JWT token.

    Args:
        data (dict[str, any]): The data to encode.
        expires_delta (int): The time in seconds for the token to expire.
        secret_key (str): The secret key to encode the token with.

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
        secret_key,
        algorithm="HS256"
    )


def decode_access_token(
        token: str,
        secret_key: str
) -> dict[str, any]:
    """
    Decodes the provided token into a dictionary.

    Args:
        token (str): The token to decode.
        secret_key (str): The secret key to decode the token with.

    Returns:
        dict[str, any]: The decoded token.
    """
    return decode(
        token,
        secret_key,
        algorithms=["HS256"]
    )


def generate_keypair(
        key_size: int
) -> tuple[PublicKey, PrivateKey]:
    """
    Generates a public and private keypair for use with the API.

    Args:
        key_size (int): The size of the keypair.

    Returns:
        tuple[str, str]: The public and private keypair.
    """
    if key_size < 2048:
        warn("Key size is less than 2048 bits, which is not recommended for security.")

    return newkeys(key_size)
