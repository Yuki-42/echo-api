"""
Initializes the auth module.
"""

# Standard Library Imports

# Third Party Imports
from dynaconf import Dynaconf

# Local Imports

# Constants
__all__ = [
    "CfAuth"
]


class CfAuth:
    """
    Authentication configuration.
    """
    __slots__ = [
        "secret_key",
        "key_expires",
        "key_size",
    ]

    def __init__(
            self,
            settings: Dynaconf
    ) -> None:
        """
        Initialises the Auth object.
        """
        self.secret_key = settings.auth.secret_key
        self.key_expires = settings.auth.key_expires
        self.key_size = settings.auth.key_size