from src.common.repository.repository import BaseRepository
from src.common.exceptions.service_exceptions import (
    UserServiceExceptionMessages, UserServiceException
)
from src.auth.utils.hasher import PasswordHasher
from src.auth.models.user import User
from src.config.core.settings import settings


from sqlalchemy.ext.asyncio import AsyncSession


class UserCreateService:


    def __init__(
            self,
            repo: BaseRepository[User, AsyncSession],
            hasher: PasswordHasher
    ) -> None:
        self.repo = repo
        self.hasher = hasher
        self.password_to_create_user = settings.token_settings.password_to_create_user

    async def create_user(self, session: AsyncSession, **kwargs) -> User:
        self._check_correct_secret_password(**kwargs)
        kwargs = self._replace_password_to_hash(**kwargs)
        instance = await self.repo.add(session, kwargs)

        return instance

    def _check_correct_secret_password(self, **kwargs) -> None:
        if kwargs.get("password_for_create_user") != self.password_to_create_user:
            raise UserServiceException(UserServiceExceptionMessages.BAD_SECRET.value)

    def _replace_password_to_hash(self, **kwargs) -> dict:
        password = kwargs.pop("password")
        kwargs["password"] = self.hasher.hash_password(password)
        kwargs.pop("password_for_create_user")
        return kwargs
