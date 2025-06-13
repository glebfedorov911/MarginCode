from fastapi import Response
from src.auth.repository.user_repository import UserRepository
from src.auth.utils.hasher import PasswordHasher
from src.auth.utils.token import TokenHandler
from src.auth.models.user import User
from src.common.exceptions.service_exceptions import UserServiceException, UserServiceExceptionMessages
from src.config.core.settings import settings

from sqlalchemy.ext.asyncio import AsyncSession


class UserAuthService:


    def __init__(self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_handler: TokenHandler,
        response: Response,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.token_handler = token_handler
        self.response = response

        self.expire_time = settings.token_settings.expires_in
        self.token_type = settings.token_settings.token_type
        self.cookie_auth_key = settings.token_settings.cookie_auth_key

    async def auth_user(self, session: AsyncSession, **kwargs) -> dict:
        user = await self._get_user_by_login(session, **kwargs)
        self._check_correct_password(user, **kwargs)
        payload = self._create_user_payload(user)
        token = self.token_handler.encode(payload, self.expire_time)
        self.response.set_cookie(self.cookie_auth_key, token)

        return {
            "token": f"{self.token_type} {token}",
        }

    async def _get_user_by_login(self, session: AsyncSession, **kwargs) -> User:
        login = kwargs.get("login")
        return await self.user_repository.get_by_login(session, login)

    def _check_correct_password(self, user: User, **kwargs) -> None:
        password = kwargs.get("password")
        if not self.password_hasher.verify_password(password, user.password):
            raise UserServiceException(UserServiceExceptionMessages.BAD_PASSWORD.value)

    @staticmethod
    def _create_user_payload(user: User) -> dict:
        return {
            "sub": str(user.id),
        }