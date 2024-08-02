"""
Contains application configuration interface.
"""
# Standard Library Imports
from pathlib import Path
from secrets import SystemRandom
from warnings import warn

# Third Party Imports
from dynaconf import Dynaconf

# Local Imports
from .models import *

# Constants
__all__ = [
    "Config",
    "CONFIG"
]

# Check if there is a secrets file
if not Path(".secrets.yaml").is_file():
    # Generate one for the users for convenience
    warn("No secrets file found. Generating one for you.")
    with open(".secrets.yaml", "w") as secrets:
        secrets.write(
            f"""
default: &default
    server:

    logging:

    database:
        password: "Developer.1"
    auth:
        secretKey: {SystemRandom().randint(0, 2 ** 256)}
        
    user_security:
        # Passwords for users 
        password_minimum_length: 10  
        password_maximum_length: 1048576  # 1 MB assuming each character is 1 byte
        password_require_uppercase: 1
        password_require_lowercase: 2
        password_require_number: 2
        password_require_special_character: 2
            
development:
    <<: *default

production:
    <<: *default
            """
        )

# Load the settings object
settings: Dynaconf = Dynaconf(
    envvar_prefix="DYNACONF",
    merge_enabled=True,
    settings_files=[".secrets.yaml", "config.yaml"],
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
        "user_security"
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


# Create the config object
CONFIG: Config = Config()
