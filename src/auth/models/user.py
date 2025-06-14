from src.config.core.base import Base
from src.common.mixin.models_mixin import DateTimeMixin

from sqlalchemy.orm import Mapped, mapped_column



class User(Base, DateTimeMixin):
    """Model for user"""

    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password: Mapped[bytes] = mapped_column(unique=True, nullable=False)
    is_staff: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)