from fastapi import APIRouter

from src.auth.router.auth import router as auth_router
from src.case.router.case import router as case_router
from src.config.core.middleware import TokenToHeaderMiddleware


router = APIRouter()

router.include_router(auth_router)
router.include_router(case_router)

middlewares = [
    TokenToHeaderMiddleware,
]