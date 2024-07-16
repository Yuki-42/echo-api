"""
Contains application configuration interface.
"""
# Standard Library Imports
from warnings import warn


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
        self.db = self.Database()

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
            warn("Database configuration is hard coded. Change IMMEDIATELY.")
            self.name = "disbroad"
            self.user = "disbroad"
            self.password = "h4ycFyEahAvjcx4tbM!guZZUqvfR3Do6-Wpm4_PFC49tPXG@LtExQQ3nihixrH.*V!h6Q.Es8Rawr6sx3--MUZCLs7sF4hVumJpx"
            self.host = "server"
            self.port = 5432
