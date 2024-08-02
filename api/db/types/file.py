"""
Contains internal file datatype.
"""

# Standard Library Imports
from uuid import UUID

# Third Party Imports
from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg.sql import Identifier

# Local Imports
from .base_type import BaseType
from .user import User
from ...models.file import File as FileModel
from ...models.user import User as UserModel

# Constants
__all__ = [
    "File"
]


class File(BaseType):
    """
    File datatype.
    """

    def __init__(
            self,
            connection: AsyncConnection,
            row: DictRow,
    ) -> None:
        """
        Initialize file.

        Args:
            connection (AsyncConnection): Connection.
            row (DictRow): Row.
        """
        # Initialize BaseType
        super(File, self).__init__(connection, row)

        self._table_name = Identifier("files")

    async def to_model(self) -> FileModel:
        """
        Convert to model.

        Returns:
            FileModel: File model.
        """
        return FileModel(
            id=self.id,
            created_at=self.created_at,
            created_by=await self.get_created_by(),
        )

    async def get_created_by_id(self) -> UUID:
        """
        Get created by id.

        Returns:
            UUID: Created by id.
        """
        # Get created_by
        row: DictRow = await self.id_get(
            column=Identifier("created_by"),
            id=self.id
        )
        return row["created_by"]

    async def get_created_by(self) -> UserModel:
        """
        Get created by.

        Returns:
            User: User.
        """
        # Get user object
        user: User = await self.users.id_get(await self.get_created_by_id())
        return await user.to_public()
