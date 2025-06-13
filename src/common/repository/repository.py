from abc import ABC
from typing import TypeVar, Type, Sequence, Tuple, Dict, Generic
import uuid

from src.common.exceptions.db_exceptions import NotFoundException, DataBaseExceptionMessages

from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy import select, Result, Select


ModelType = TypeVar('ModelType')
SessionType = TypeVar("SessionType")

class BaseRepository(Generic[ModelType, SessionType], ABC):
    """Base repository for another repositories"""

    def __init__(self, model: Type[ModelType]):
        """
        Constructor
        :param model: model for repository
        """
        self.model = model

    async def get_by_id(self, session: AsyncSession, id_: uuid.UUID) -> ModelType:
        """
        Method for get record by id
        :param session: session for work with db
        :param id_: the id value that is being searched for
        :return: record with this id
        """
        stmt = select(self.model).where(self.model.id==id_)
        records = await self._get_result(session, stmt)
        return self._get_one_record_from_sequence(records, id_)

    async def get_all(self, session: AsyncSession, offset: int = 0, limit: int = 10) -> Tuple[int, Sequence[ModelType]]:
        """
        Method for get all records
        :param session: session for work with db
        :param offset: offset of records
        :param limit: limit of records
        :return: count records and sequence of records
        """
        stmt = select(self.model).offset(offset).limit(limit)
        records = await self._get_result(session, stmt)
        return len(records), records

    async def add(self, session: AsyncSession, data_add: Dict) -> ModelType:
        """
        Method for add record
        :param session: session for work with db
        :param data_add: dictionary with data for add in model
        :return: added data
        """
        instance = self.model(**data_add)
        session.add(instance)
        await self._commit_and_refresh_base(session, instance)
        return instance

    async def update(self, session: AsyncSession, id_: uuid.UUID, data_update: Dict) -> ModelType:
        """
        Method for update record
        :param session: session for work with db
        :param id_: the id value that is being searched for
        :param data_update: dictionary with data for update in model
        :return: updated data
        """
        instance = self.get_by_id(session, id_)
        instance = self._update_data_in_instance(instance, data_update)
        await self._commit_and_refresh_base(session, instance)
        return instance

    async def delete(self, session: AsyncSession, id_: uuid.UUID) -> None:
        """
        Method for delete record
        :param session: session for work with db
        :param id_: the id value that is being searched for
        :return: None
        """
        instance = self.get_by_id(session, id_)
        await session.delete(instance)
        await self._commit_and_refresh_base(session)

    @staticmethod
    async def _get_result(session: AsyncSession, stmt: Select) -> Sequence[ModelType]:
        """
        Method for get result
        :param session: session for work with db
        :param stmt: query 
        :return: sequence of records
        """
        result: Result = await session.execute(stmt)
        return result.scalars().all()

    def _get_one_record_from_sequence(self, records: Sequence[ModelType], val: any) -> ModelType:
        """
        Method for check has records in sequence
        :param records: sequence of records
        :param id_: the id value that is being searched for
        :return: founded record
        """
        if not records:
            exc_msg = DataBaseExceptionMessages.NOT_FOUND_BY.value % (val, self.model.__tablename__)
            raise NotFoundException(exc_msg)
        return records[0]

    @staticmethod
    async def _commit_and_refresh_base(session: AsyncSession, instance: ModelType | None = None) -> None:
        """
        Method for update base
        :param session: session for work with db
        :param instance: data added/updated in model
        :return: None
        """
        await session.commit()
        if instance is not None:
            await session.refresh(instance)

    @staticmethod
    def _update_data_in_instance(instance: ModelType, data_update: Dict) -> ModelType:
        """
        Method for update data
        :param instance: data from database
        :param data_update: dictionary with data for update in model
        :return: updated data
        """
        for key, value in data_update.items():
            if value is not None:
                setattr(instance, key, value)
        return instance