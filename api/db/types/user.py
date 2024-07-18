"""
Contains internal user datatype.
"""
# Standard Library Imports
from datetime import datetime
from uuid import UUID

# Third Party Imports
from psycopg2.extras import DictConnection, DictCursor, DictRow
from psycopg2.sql import Identifier

# Local Imports
from .base_type import BaseType
from ...models.user import User as PublicUser, PrivateUser, Token, Device

# Constants
__all__ = ["User"]


class User(BaseType):
    """
    User datatype.
    """

    def __init__(
            self,
            connection: DictConnection,
            row: DictRow,
    ) -> None:
        # Initialize BaseType
        super(User, self).__init__()

        self._connection = connection
        self._table_name = Identifier("users")

        # Set attributes
        self.id = UUID(row["id"])
        self.created_at = row["created_at"]

    def to_public(self) -> PublicUser:
        """
        Convert to model.

        Returns:
            UserModel: User model.
        """
        return PublicUser(
            id=self.id,
            created_at=self.created_at,
            email=self.email,
            username=self.username,
            icon=self.icon,
            bio=self.bio,
            last_online=self.last_online,
            is_online=self.is_online,
            is_banned=self.is_banned,
            is_verified=self.is_verified
        )

    def to_private(self) -> PrivateUser:
        """
        Convert to private model.

        Returns:
            UserModel: User model.
        """
        return PrivateUser(
            id=self.id,
            created_at=self.created_at,
            email=self.email,
            username=self.username,
            icon=self.icon,
            bio=self.bio,
            last_online=self.last_online,
            is_online=self.is_online,
            is_banned=self.is_banned,
            is_verified=self.is_verified,
            tokens=self.tokens,
            password_last_updated=self.password_last_updated
        )

    @property
    def email(self) -> str:
        """
        Get email.

        Returns:
            str: Email.
        """
        # Get email
        cursor: DictCursor = self.id_get(
            column=Identifier("email"),
            id=str(self.id)
        )

        return cursor.fetchone()["email"]

    @email.setter
    def email(self, value: str) -> None:
        """
        Set email.

        Args:
            value (str): Email.

        Returns:
            None
        """
        # Set email
        self.id_set(
            column=Identifier("email"),
            id=self.id,
            value=value
        )

    @property
    def username(self) -> str:
        """
        Get username.

        Returns:
            str: Username.
        """
        # Get username
        cursor: DictCursor = self.id_get(
            column=Identifier("username"),
            id=self.id
        )

        return cursor.fetchone()["username"]

    @username.setter
    def username(self, value: str) -> None:
        """
        Set username.

        Args:
            value (str): Username.

        Returns:
            None
        """
        # Set username
        self.id_set(
            column=Identifier("username"),
            id=self.id,
            value=value
        )

    @property
    def icon_id(self) -> UUID:
        """
        Get icon.

        Returns:
            UUID: Icon.
        """
        # Get icon
        cursor: DictCursor = self.id_get(
            column=Identifier("icon"),
            id=self.id
        )

        return cursor.fetchone()["icon"]  # TODO: Ensure that this is an actual UUID

    @icon_id.setter
    def icon_id(self, value: UUID) -> None:
        """
        Set icon.

        Args:
            value (UUID): Icon.

        Returns:
            None
        """
        #

    @property
    def icon(self):
        """
        Get icon.

        Returns:
            Icon: Icon.
        """
        # Create new transaction
        raise NotImplementedError("Icon property not implemented.")  # TODO: Implement icon property

    @property
    def bio(self) -> str:
        """
        Get bio.

        Returns:
            str: Bio.
        """
        # Get bio
        cursor: DictCursor = self.id_get(
            column=Identifier("bio"),
            id=self.id
        )

        return cursor.fetchone()["bio"]

    @bio.setter
    def bio(self, value: str) -> None:
        """
        Set bio.

        Args:
            value (str): Bio.
        """
        # Set bio
        self.id_set(
            column=Identifier("bio"),
            id=self.id,
            value=value
        )

    @property
    def last_online(self) -> datetime:
        # Get last_online
        cursor: DictCursor = self.id_get(
            column=Identifier("last_online"),
            id=self.id
        )
        return datetime.strptime(cursor.fetchone()["last_online"], "%Y-%m-%d %H:%M:%S.%f")

    @last_online.setter
    def last_online(self, value: datetime) -> None:
        """
        Set last online.

        Args:
            value (datetime): Last online.
        """
        # Set last_online
        self.id_set(
            column=Identifier("last_online"),
            id=self.id,
            value=value
        )

    @property
    def is_online(self) -> bool:
        """
        Get online status.

        Returns:
            bool: Online status.
        """
        # Get is_online
        cursor: DictCursor = self.id_get(
            column=Identifier("is_online"),
            id=self.id
        )

        return cursor.fetchone()["is_online"]

    @is_online.setter
    def is_online(self, value: bool) -> None:
        """
        Set online status.

        Args:
            value (bool): Online status.
        """
        # Set is_online
        self.id_set(
            column=Identifier("is_online"),
            id=self.id,
            value=value
        )

    @property
    def is_banned(self) -> bool:
        """
        Get ban status.

        Returns:
            bool: Ban status.
        """
        # Get is_banned
        cursor: DictCursor = self.id_get(
            column=Identifier("is_banned"),
            id=self.id
        )

        return cursor.fetchone()["is_banned"]

    @is_banned.setter
    def is_banned(self, value: bool) -> None:
        """
        Set ban status.

        Args:
            value (bool): Ban status.
        """
        # Set is_banned
        self.id_set(
            column=Identifier("is_banned"),
            id=self.id,
            value=value
        )

    @property
    def is_verified(self) -> bool:
        """
        Get verified status.

        Returns:
            bool: Verified status.
        """
        # Get is_verified
        cursor: DictCursor = self.id_get(
            column=Identifier("is_verified"),
            id=self.id
        )

        return cursor.fetchone()["is_verified"]

    @is_verified.setter
    def is_verified(self, value: bool) -> None:
        """
        Set verified status.

        Args:
            value (bool): Verified status.
        """
        # Set is_verified
        self.id_set(
            column=Identifier("is_verified"),
            id=self.id,
            value=value
        )

    @property
    def tokens(self) -> list[Token]:
        """
        Get tokens.

        Returns:
            list: Tokens.
        """
        # Get tokens
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM secured.tokens WHERE user_id = %s;",
                [self.id]
            )

            token_data: list[DictRow] = cursor.fetchall()

        # Get devices
        for token in token_data:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM secured.devices WHERE id = %s;",
                    [token["device_id"]]
                )
                device_data: DictRow = cursor.fetchone()
                token["device"] = Device(
                    id=device_data["id"],
                    created_at=datetime.strptime(device_data["created_at"], "%Y-%m-%d %H:%M:%S.%f"),
                    name=device_data["name"],
                    ip=device_data["ip"],
                    mac=device_data["mac"],
                    lang=device_data["lang"],
                    os=device_data["os"],
                    screen_size=device_data["screen_size"],
                    country=device_data["country"]
                )

        return [Token(
            user=self,
            device=Device(
                id=UUID(token["device_id"]),
                created_at=datetime.strptime(token["created_at"], "%Y-%m-%d %H:%M:%S.%f"),
                name=token["name"],
                ip=token["ip"],
                mac=token["mac"],
                lang=token["lang"],
                os=token["os"],
                screen_size=token["screen_size"],
                country=token["country"]
            ),
            token=token["token"],
            last_used=datetime.strptime(token["last_used"], "%Y-%m-%d %H:%M:%S.%f")
        ) for token in token_data]

    @property
    def password_last_updated(self) -> datetime:
        """
        Get password last updated.

        Returns:
            datetime: Password last updated.
        """
        # Create cursor
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT last_updated FROM secured.passwords WHERE user_id = %s;",
                [self.id]
            )

            return datetime.strptime(cursor.fetchone()["last_updated"], "%Y-%m-%d %H:%M:%S.%f")
