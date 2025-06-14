from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
import pydantic_core

from typing import List

from src.config.core.settings import settings
from src.config.core.db_helper import database_helper
from src.case.schemas.case import (
    CaseRead, CaseCreate, CaseUpdate
)
from src.case.dependency.service_depend import (
    get_case_create_service, get_update_create_service
)
from src.case.service.case_create_service import CaseCreateService
from src.case.service.case_update_service import CaseUpdateService
from src.case.repository.case_repository import CaseRepository
from src.case.dependency.repository_depend import get_case_repository
from src.auth.dependency.service_depend import get_user_current_service


router = APIRouter(
    prefix=settings.router_settings.case_prefix,
    tags=[settings.router_settings.case_tag]
)

async def check_rules_user(current_user, session: AsyncSession):
    current_user = await current_user.current_user(session)
    if not current_user.is_staff:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to perform this action",
        )

@router.post("/")
async def create_case(
    case: str = Form(...),
    file: List[UploadFile] | None = File(None),
    session: AsyncSession = Depends(database_helper.session_depends),
    service: CaseCreateService = Depends(get_case_create_service),
    current_user = Depends(get_user_current_service),
) -> CaseRead:
    """Case - string format: {"title":"string","description":"string","price":float}"""
    try:
        await check_rules_user(current_user, session)

        case = CaseCreate.model_validate_json(case)
        case_collection = case.model_dump()
        case_collection["images"] = file if file else []
        return await service.create_case(session, **case_collection)
    except HTTPException as e:
        raise e
    except pydantic_core._pydantic_core.ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as e:
        print(e)
        if hasattr(e, "code") and isinstance(e.code, int):
            raise HTTPException(status_code=e.code, detail=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/")
async def read_cases(
    offset: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(database_helper.session_depends),
    repo: CaseRepository = Depends(get_case_repository),
):
    try:
        count_records, records = await repo.get_all(session, offset=offset, limit=limit)
        return {
            "count": count_records,
            "records": [CaseRead(**record.to_dict()) for record in records],
        }
    except HTTPException as e:
        raise e
    except pydantic_core._pydantic_core.ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as e:
        if hasattr(e, "code") and isinstance(e.code, int):
            raise HTTPException(status_code=e.code, detail=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/{id}")
async def update_case(
    id: str,
    case: str | None = Form(None),
    file: List[UploadFile] | None = File(None),
    session: AsyncSession = Depends(database_helper.session_depends),
    service: CaseUpdateService = Depends(get_update_create_service),
    current_user=Depends(get_user_current_service),
) -> CaseRead:
    """Case - string format: {"title":"string","description":"string","price":float}"""
    try:
        await check_rules_user(current_user, session)

        case = CaseUpdate.model_validate_json(case)
        case_collection = case.model_dump()
        case_collection["images"] = file if file else []
        return await service.update_case(session, id, **case_collection)
    except HTTPException as e:
        raise e
    except pydantic_core._pydantic_core.ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as e:
        if hasattr(e, "code") and isinstance(e.code, int):
            raise HTTPException(status_code=e.code, detail=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{id}")
async def delete_case(
    id: str,
    session: AsyncSession = Depends(database_helper.session_depends),
    repo: CaseRepository = Depends(get_case_repository),
    current_user=Depends(get_user_current_service),
):
    try:
        await check_rules_user(current_user, session)

        return await repo.delete(session, id)
    except HTTPException as e:
        raise e
    except pydantic_core._pydantic_core.ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as e:
        if hasattr(e, "code") and isinstance(e.code, int):
            raise HTTPException(status_code=e.code, detail=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
