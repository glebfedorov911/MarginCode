from fastapi import APIRouter

from src.auth.router.auth import router as auth_router
from src.config.core.middleware import TokenToHeaderMiddleware


router = APIRouter()

router.include_router(auth_router)

middlewares = [
    TokenToHeaderMiddleware,
]