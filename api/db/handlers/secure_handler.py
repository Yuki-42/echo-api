"""
Contains the secure handler.
"""

# Standard Library Imports

# Third Party Imports

# Local Imports
from .base_handler import BaseHandler
from ...security.scheme import crypt_context


# Constants


class SecureHandler(BaseHandler):
    """
    Secure handler.
    """

    @staticmethod
    def hash_password(
            password: str
    ) -> str:
        """
        Hash a password.

        Args:
            password (str): Password.

        Returns:
            str: Hashed password.
        """
        return crypt_context.hash(password)

    @staticmethod
    def verify_password(
            password: str,
            hashed_password: str
    ) -> bool:
        """
        Verify a password.

        Args:
            password (str): Password.
            hashed_password (str): Hashed password.

        Returns:
            bool: Verification.
        """
        return crypt_context.verify(password, hashed_password)
