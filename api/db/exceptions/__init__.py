"""
Initialises the exceptions module.
"""

# Standard Library Imports

# Third Party Imports

# Local Imports
from .users import UserDoesNotExist, UserAlreadyExists

# Constants
__all__ = [
    "UserDoesNotExist",
    "UserAlreadyExists",
]
