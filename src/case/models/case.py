from src.common.mixin.models_mixin import DateTimeMixin
from src.config.core.base import Base

from typing import List

from sqlalchemy.orm import Mapped, mapped_column



class Case(Base, DateTimeMixin):
    """Model for case"""

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    images: Mapped[List[str]] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
