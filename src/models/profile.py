import datetime
from functools import partial

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ProfileModel(Base):
    __tablename__ = "profiles"
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True, nullable=True)
    first_name: Mapped[str] = mapped_column(default="")
    last_name: Mapped[str] = mapped_column(default="")
    birth_date: Mapped[datetime.date] = mapped_column(nullable=True)

    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=partial(datetime.datetime.now, datetime.timezone.utc),
        onupdate=partial(datetime.datetime.now, datetime.timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Profile {self.email}>"
