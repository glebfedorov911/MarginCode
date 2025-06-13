from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.config.core.settings import settings


class DataBaseHelper:
    """Class for work with sessions"""
    AUTOFLUSH=False
    AUTOCOMMIT=False
    EXPIRE_ON_COMMIT=False


    def __init__(
            self,
            *,
            url: str,
            echo: bool,
    ) -> None:
        self.engine = create_async_engine(url, echo=echo)

        self.session_maker = async_sessionmaker(
            bind=self.engine,
            autoflush=self.AUTOFLUSH,
            autocommit=self.AUTOCOMMIT,
            expire_on_commit=self.EXPIRE_ON_COMMIT,
        )

    async def session_depends(self) -> AsyncGenerator[AsyncSession, None]:
        """Generator for session"""
        async with self.session_maker() as session:
            yield session

database_helper = DataBaseHelper(
    url=settings.database_settings.url,
    echo=settings.database_settings.echo,
)