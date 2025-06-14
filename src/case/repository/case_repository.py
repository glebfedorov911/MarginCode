from src.common.repository.repository import BaseRepository
from src.case.models.case import Case

from sqlalchemy.ext.asyncio import AsyncSession


class CaseRepository(BaseRepository[Case, AsyncSession]):


    def __init__(self):
        super().__init__(Case)