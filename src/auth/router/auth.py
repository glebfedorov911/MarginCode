from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.core.settings import settings
from src.config.core.db_helper import database_helper
from src.auth.schemas.user import UserCreate, UserRead, UserAuth
from src.auth.service.user_create_service import UserCreateService
from src.auth.service.user_auth_service import UserAuthService
from src.auth.dependency.service_depend import (
    get_user_create_service, get_user_auth_service, get_user_current_service
)

router = APIRouter(
    prefix=settings.router_settings.auth_prefix,
    tags=[settings.router_settings.auth_tag],
)

@router.post("/create-user")
async def create_user(
        user_create: UserCreate,
        service: UserCreateService = Depends(get_user_create_service),
        session: AsyncSession = Depends(database_helper.session_depends)
    ) -> UserRead:
        try:
            return await service.create_user(session, **user_create.model_dump())
        except HTTPException as e:
            raise e
        except Exception as e:
            if hasattr(e, "code"):
                print(e.code)
                raise HTTPException(status_code=e.code, detail=str(e))
            raise HTTPException(status_code=400, detail="Bad request")

@router.post("/login-user")
async def login(
        user_auth: UserAuth,
        response: Response,
        service: UserAuthService = Depends(get_user_auth_service),
        session: AsyncSession = Depends(database_helper.session_depends)
) -> dict:
    try:
        return await service.auth_user(session, **user_auth.model_dump())
    except HTTPException as e:
        raise e
    except Exception as e:
        if hasattr(e, "code"):
            raise HTTPException(status_code=e.code, detail=str(e))
        raise HTTPException(status_code=400, detail="Bad request")

@router.get("/current-user")
async def current_user(
        request: Request,
        service = Depends(get_user_current_service),
        session: AsyncSession = Depends(database_helper.session_depends),
) -> UserRead:
    try:
        return await service.current_user(session)
    except HTTPException as e:
        raise e
    except Exception as e:
        if hasattr(e, "code") and isinstance(e.code, int):
            raise HTTPException(status_code=e.code, detail=str(e))
        raise HTTPException(status_code=400, detail="Bad request")