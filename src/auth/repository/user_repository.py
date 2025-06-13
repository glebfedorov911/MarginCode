from src.common.repository.repository import BaseRepository
from src.auth.models.user import User

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, AsyncSession]):


    def __init__(self):
        super().__init__(User)

    async def get_by_login(self, session: AsyncSession, login: str) -> User:
        """
        Method for get record by login
        :param session: session for work with db
        :param login: user login
        :return: record
        """
        stmt = select(self.model).where(self.model.login == login)
        records = await self._get_result(session, stmt)
        return self._get_one_record_from_sequence(records, login)