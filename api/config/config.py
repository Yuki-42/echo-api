"""
Contains application configuration interface.
"""
# Standard Library Imports
from pathlib import Path
from os import getcwd
from secrets import SystemRandom
from warnings import warn

# Third Party Imports
from dynaconf import Dynaconf
from rsa import PrivateKey, PublicKey

# Local Imports
from .models import *
from ..security.scheme import generate_keypair

# Constants
__all__ = [
    "Config",
    "CONFIG"
]
CWD: Path = Path(getcwd())

# Check if there is a secrets file
if not Path(CWD, "config", ".secrets.yaml").is_file():
    # Generate one for the users for convenience
    warn("No secrets file found. Generating one for you.")

    # Generate a new keypair for the server owner
    keypair: tuple[PublicKey, PrivateKey] = generate_keypair(2048)

    # Generate the secrets file contents outside of the with statement so that the info can be logged
    contents: str = f"""
default: &default
    server:

    logging:

    database:
        password: "Developer.1"
    auth:
        secret_key: {SystemRandom().randint(0, 2 ** 256)}
            
development:
    <<: *default

production:
    <<: *default
            """
    with open(Path(CWD, "config", ".secrets.yaml"), "w") as secrets:
        secrets.write(
            contents
        )

    # Write the public key to the server owner's public key file
    with open(Path(CWD, "config", "owner_public_key.pem"), "wb") as public_key_file:
        public_key_file.write(keypair[0].save_pkcs1())

    # Write the private key to the server owner's private key file
    with open(Path(CWD, "config", "owner_private_key.pem"), "wb") as private_key_file:
        private_key_file.write(keypair[1].save_pkcs1())

# Load the settings object
settings: Dynaconf = Dynaconf(
    envvar_prefix="DYNACONF",
    merge_enabled=True,
    settings_files=[
        Path(CWD, "config", ".secrets.yaml"),
        Path(CWD, "config", "config.yaml")
    ],
    load_dotenv=True,
    environments=True,
    env_switcher="development",
    lowercase_read=True
)


class Config:
    """
    Stores application wide configuration data.
    """
    __slots__ = [
        "db",
        "auth",
        "user_security",
        "server"
    ]

    def __init__(
            self
    ) -> None:
        """
        Initialises the Config object.
        """
        self.db = CfDatabase(settings)
        self.auth = CfAuth(settings)
        self.user_security = CfUserSecurity(settings)
        self.server = CfServer(settings)


# Create the config object
CONFIG: Config = Config()
