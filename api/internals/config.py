"""
Contains application configuration interface.
"""
# Standard Library Imports
from secrets import SystemRandom
from warnings import warn
from pathlib import Path

# Third Party Imports
from dynaconf import Dynaconf

# Local Imports

# Constants
__all__ = [
    "Config"
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
        secretKey: {SystemRandom().randint(0, 2**256)}

    logging:

    database:
        password: "Developer.1"

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
        "db"
    ]

    def __init__(
            self
    ) -> None:
        """
        Initialises the Config object.
        """
        self.db = self.Database()

    class Server:
        """
        Server configuration.
        """
        __slots__ = [
            "secretKey",
        ]

        def __init__(
                self
        ) -> None:
            """
            Initialises the Server object.
            """
            self.secretKey = settings.server.secretKey

    class Database:
        """
        Database configuration.
        """
        __slots__ = [
            "name",
            "user",
            "password",
            "host",
            "port"
        ]

        def __init__(
                self
        ) -> None:
            self.name = settings.database.name
            self.user = settings.database.user
            self.host = settings.database.host
            self.port = settings.database.port
            self.password = settings.database.password

