"""
Initializes the user_security module.
"""

# Standard Library Imports

# Third Party Imports
from dynaconf import Dynaconf

# Local Imports

# Constants
__all__ = [
    "CfUserSecurity"
]


class CfUserSecurity:
    """
    User security configuration.
    """
    __slots__ = [
        "password_minimum_length",
        "password_maximum_length",
        "password_require_uppercase",
        "password_require_lowercase",
        "password_require_number",
        "password_require_special_character",
    ]

    def __init__(
            self,
            settings: Dynaconf
    ) -> None:
        self.password_minimum_length: str = settings.user_security.password_minimum_length
        self.password_maximum_length: str = settings.user_security.password_maximum_length
        self.password_require_uppercase: int = settings.user_security.require_uppercase
        self.password_require_lowercase: int = settings.user_security.require_lowercase
        self.password_require_number: int = settings.user_security.require_number
        self.password_require_special_character: int = settings.user_security.require_special_character
