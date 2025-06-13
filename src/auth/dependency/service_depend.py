from fastapi import Depends, Response, Request

from src.auth.dependency.token_depend import get_pyjwt_token_handler
from src.auth.service.user_create_service import UserCreateService
from src.auth.service.user_auth_service import UserAuthService
from src.auth.service.user_current_service import UserCurrentService
from src.auth.utils.hasher import PasswordHasher
from src.auth.dependency.hasher_depend import get_password_hasher
from src.auth.dependency.repository_depend import get_user_repository
from src.auth.utils.token import TokenHandler
from src.common.repository.repository import BaseRepository
from src.auth.repository.user_repository import UserRepository


def get_user_create_service(
        repo: BaseRepository = Depends(get_user_repository),
        hasher: PasswordHasher = Depends(get_password_hasher),
) -> UserCreateService:
    return UserCreateService(repo, hasher)

def get_user_auth_service(
    response: Response,
    repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    token: TokenHandler = Depends(get_pyjwt_token_handler),
) -> UserAuthService:
    return UserAuthService(repo, hasher, token, response)

def get_user_current_service(
    request: Request,
    repo: UserRepository = Depends(get_user_repository),
    token: TokenHandler = Depends(get_pyjwt_token_handler),
) -> UserCurrentService:
    return UserCurrentService(repo, token, request)