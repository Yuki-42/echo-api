"""
Contains internal user datatype.
"""
# Standard Library Imports
from datetime import datetime
from uuid import UUID

# Third Party Imports
from psycopg2.extras import DictConnection, DictRow

# Local Imports
from .base_type import BaseType
from ...models.user import User as UserModel

# Constants
__all__ = ["User"]


class User(UserModel, BaseType):
    """
    User datatype.
    """

    def __init__(
            self,
            connection: DictConnection,
            row: DictRow,
    ) -> None:
        super(User, self).__init__()
        self._connection = connection

        # Set attributes
        self.id = UUID(row["id"])
        self.created_at = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S.%f")

    def to_model(self) -> UserModel:
        """
        Convert to model.

        Returns:
            UserModel: User model.
        """
        return UserModel(
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

    @property
    def email(self) -> str:
        """
        Get email.

        Returns:
            str: Email.
        """
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Get email
            cursor.execute(
                """
                SELECT email
                FROM public.users
                WHERE id = %s;
                """,
                (self.id,)
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
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Update email
            cursor.execute(
                """
                UPDATE public.users
                SET email = %s
                WHERE id = %s;
                """,
                (value, self.id)
            )

    @property
    def username(self) -> str:
        """
        Get username.

        Returns:
            str: Username.
        """
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Get username
            cursor.execute(
                """
                SELECT username
                FROM public.users
                WHERE id = %s;
                """,
                (self.id,)
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
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Update username
            cursor.execute(
                """
                UPDATE public.users
                SET username = %s
                WHERE id = %s;
                """,
                (value, self.id)
            )

    @property
    def icon_id(self) -> UUID:
        """
        Get icon.

        Returns:
            UUID: Icon.
        """
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Get icon
            cursor.execute(
                """
                SELECT icon
                FROM public.users
                WHERE id = %s;
                """,
                (self.id,)
            )
            return UUID(cursor.fetchone()["icon"])

    @icon_id.setter
    def icon_id(self, value: UUID) -> None:
        """
        Set icon.

        Args:
            value (UUID): Icon.

        Returns:
            None
        """
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Update icon
            cursor.execute(
                """
                UPDATE public.users
                SET icon = %s
                WHERE id = %s;
                """,
                (value, self.id)
            )

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
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Get bio
            cursor.execute(
                """
                SELECT bio
                FROM public.users
                WHERE id = %s;
                """,
                (self.id,)
            )
            return cursor.fetchone()["bio"]

    @bio.setter
    def bio(self, value: str) -> None:
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Update bio
            cursor.execute(
                """
                UPDATE public.users
                SET bio = %s
                WHERE id = %s;
                """,
                (value, self.id)
            )

    @property
    def last_online(self) -> datetime:
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Get last_online
            cursor.execute(
                """
                SELECT last_online
                FROM public.users
                WHERE id = %s;
                """,
                (self.id,)
            )
            return datetime.strptime(cursor.fetchone()["last_online"], "%Y-%m-%d %H:%M:%S.%f")

    @last_online.setter
    def last_online(self, value: datetime) -> None:
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Update last_online
            cursor.execute(
                """
                UPDATE public.users
                SET last_online = %s
                WHERE id = %s;
                """,
                (value, self.id)
            )

    @property
    def is_online(self) -> bool:
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Get is_online
            cursor.execute(
                """
                SELECT is_online
                FROM public.users
                WHERE id = %s;
                """,
                (self.id,)
            )
            return cursor.fetchone()["is_online"]
        
    @is_online.setter
    def is_online(self, value: bool) -> None:
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Update is_online
            cursor.execute(
                """
                UPDATE public.users
                SET is_online = %s
                WHERE id = %s;
                """,
                (value, self.id)
            )
            
    @property
    def is_banned(self) -> bool:
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Get is_banned
            cursor.execute(
                """
                SELECT is_banned
                FROM public.users
                WHERE id = %s;
                """,
                (self.id,)
            )
            return cursor.fetchone()["is_banned"]
        
    @is_banned.setter
    def is_banned(self, value: bool) -> None:
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Update is_banned
            cursor.execute(
                """
                UPDATE public.users
                SET is_banned = %s
                WHERE id = %s;
                """,
                (value, self.id)
            )
            
    @property
    def is_verified(self) -> bool:
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Get is_verified
            cursor.execute(
                """
                SELECT is_verified
                FROM public.users
                WHERE id = %s;
                """,
                (self.id,)
            )
            return cursor.fetchone()["is_verified"]
        
    @is_verified.setter
    def is_verified(self, value: bool) -> None:
        # Create new transaction
        with self.connection.cursor() as cursor:
            # Update is_verified
            cursor.execute(
                """
                UPDATE public.users
                SET is_verified = %s
                WHERE id = %s;
                """,
                (value, self.id)
            )
            