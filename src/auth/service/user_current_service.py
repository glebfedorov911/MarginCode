
from src.auth.repository.user_repository import UserRepository
from src.auth.utils.token import TokenHandler
from src.auth.models.user import User
from src.common.exceptions.service_exceptions import UserServiceExceptionMessages
from src.config.core.settings import settings

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Response, status, HTTPException


class UserCurrentService:


    def __init__(
            self,
            repo: UserRepository,
            token_handler: TokenHandler,
            request: Request,
    ):
        self.repo = repo
        self.token_handler = token_handler
        self.request = request
        self.header_token = settings.token_settings.token_header
        self.exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UserServiceExceptionMessages.CREDENTIAL.value,
            headers={"WWW-Authenticate": settings.token_settings.token_header},
        )

    async def current_user(self, session: AsyncSession) -> User:
        token = self.request.headers.get(self.header_token)
        if not token:
            raise self.exc
        token = token.split(" ")[1]
        payload = self.token_handler.decode(token)
        if (sub := payload.get("sub", None)) is None:
            raise self.exc

        return await self.repo.get_by_id(session, sub)