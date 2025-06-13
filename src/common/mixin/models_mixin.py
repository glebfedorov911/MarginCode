from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column


class DateTimeMixin:

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
