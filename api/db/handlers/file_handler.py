"""
Contains the Files handler.
"""

# Standard Library Imports
from uuid import UUID

# Third Party Imports
from psycopg import AsyncCursor
from psycopg.rows import DictRow
from psycopg.sql import SQL

# Local Imports
from .base_handler import BaseHandler
from ..types.file import File

# Constants
__all__ = [
    "FilesHandler",
]


class FilesHandler(BaseHandler):
    """
    Files handler.
    """

    async def id_get(
            self,
            file_id: UUID
    ) -> File | None:
        """
        Get file by ID.

        Args:
            file_id (UUID): File ID.

        Returns:
            File: File.
        """
        # Create a cursor
        cursor: AsyncCursor
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                SQL(
                    r"SELECT id, created_at FROM files WHERE id = %s;  /* Only select the unchanging columns, everything else is grabbed on-request */",
                ),
                [
                    file_id,
                ]
            )
            row: DictRow = await cursor.fetchone()

        if row is None:
            return None

        # Return
        return File(
            connection=self.connection,
            row=row,
        )
