"""
Initializes the database module.
"""

# Standard Library Imports

# Third Party Imports
from dynaconf import Dynaconf

# Local Imports

# Constants
__all__ = [
    "CfDatabase"
]


class CfDatabase:
    """
    Database model for config parsing.
    """
    __slots__ = [
        "name",
        "user",
        "password",
        "host",
        "port"
    ]

    def __init__(
            self,
            settings: Dynaconf
    ) -> None:
        self.name = settings.database.name
        self.user = settings.database.user
        self.host = settings.database.host
        self.port = settings.database.port
        self.password = settings.database.password
