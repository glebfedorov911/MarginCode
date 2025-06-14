from sqlalchemy.ext.asyncio import AsyncSession

from src.case.repository.case_repository import CaseRepository
from src.case.models.case import Case
from src.case.service.mixin import CaseServiceMixin


class CaseCreateService(CaseServiceMixin):


    def __init__(
            self,
            repo: CaseRepository,
    ):
        super().__init__(repo)

    async def create_case(self, session: AsyncSession, **kwargs) -> Case:
        kwargs = self._work_with_images(**kwargs)
        return await self.repo.add(session, kwargs)