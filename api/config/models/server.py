"""
Initializes the server module.
"""

# Standard Library Imports
from os import getcwd
from pathlib import Path
from rsa import PublicKey, PrivateKey

# Third Party Imports
from dynaconf import Dynaconf

# Local Imports

# Constants
__all__ = [
    "CfServer"
]


class CfServer:
    """
    Server configuration.
    """
    __slots__ = [
        "owner_public_key",
        "owner_private_key",
    ]

    def __init__(
            self,
            settings: Dynaconf
    ) -> None:
        """
        Initialises the Server object.
        """
        # Public and private key are stored in config folder
        self.owner_public_key = Path(getcwd(), "config", "owner_public_key.pem")
        self.owner_private_key = Path(getcwd(), "config", "owner_private_key.pem")

        # Check if the keys exist
        if not self.owner_public_key.is_file():
            raise FileNotFoundError(f"Public key not found at {self.owner_public_key}")

        if not self.owner_private_key.is_file():
            raise FileNotFoundError(f"Private key not found at {self.owner_private_key}")

        # Read in the keys
        with open(self.owner_public_key, "rb") as public_key:
            self.owner_public_key: PublicKey = PublicKey.load_pkcs1(public_key.read())

        with open(self.owner_private_key, "rb") as private_key:
            self.owner_private_key: PrivateKey = PrivateKey.load_pkcs1(private_key.read())
