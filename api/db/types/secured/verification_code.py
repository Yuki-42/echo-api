"""
Contains the verification code datatype
"""
from uuid import UUID

# Standard Library Imports

# Third Party Imports
from psycopg import AsyncConnection
from psycopg.rows import DictRow
from psycopg.sql import Identifier

# Local Imports
from ..base_type import BaseType
from ..user import User
from ....models.secure import VerificationCode as VerificationCodeModel
from ....models.user import User as UserModel

# Constants
__all__ = [

]


class VerificationCode(BaseType):
    """
    Verification code datatype.
    """

    def __init__(
            self,
            connection: AsyncConnection,
            row: DictRow,
    ) -> None:
        """
        Initialize verification code.

        Args:
            connection (AsyncConnection): Connection.
            row (DictRow): Row.
        """
        # Initialize BaseType
        super().__init__(connection, row)

        self._table_name = Identifier("secured.verification_codes")

    async def to_model(self) -> VerificationCodeModel:
        """
        Convert to model.

        Returns:
            VerificationCodeModel: Verification code model.
        """
        return VerificationCodeModel(
            id=self.id,
            created_at=self.created_at,
            user=await self.get_user(),
            code=await self.get_code(),
            expires=await self.get_expires(),
        )

    async def get_user_id(self) -> UUID:
        """
        Get user id.

        Returns:
            UUID: User id.
        """
        # Get user id
        row: DictRow = await self.id_get(
            column=Identifier("user_id"),
            id=self.id
        )
        return row["user_id"]

    async def get_user(self) -> UserModel:
        """
        Get user.

        Returns:
            UserModel: User.
        """
        # Get user
        user_id: UUID = await self.get_user_id()

        # Get user object
        user: User = await self.users.id_get(user_id)
        return await user.to_public()
