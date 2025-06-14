from fastapi import Depends

from src.case.service.case_create_service import CaseCreateService
from src.case.service.case_update_service import CaseUpdateService
from src.case.repository.case_repository import CaseRepository
from src.case.dependency.repository_depend import get_case_repository


def get_case_create_service(
        repo: CaseRepository = Depends(get_case_repository),
) -> CaseCreateService:
    return CaseCreateService(repo)

def get_update_create_service(
        repo: CaseRepository = Depends(get_case_repository),
) -> CaseUpdateService:
    return CaseUpdateService(repo)