from sqlalchemy.orm import Mapped, mapped_column, declared_attr, DeclarativeBase

import uuid


class Base(DeclarativeBase):
    """Base class for all model of project"""
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """This method generate table name"""
        return f"{cls.__name__.lower()}s"

    def to_dict(self) -> dict:
        """Convert the model instance to a dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True, autoincrement=False
    )