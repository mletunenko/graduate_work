import datetime
from functools import partial

from sqlalchemy import TIMESTAMP, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.enums import UserRoleEnum

from .base import Base


class ProfileModel(Base):
    __tablename__ = "profiles"
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True, nullable=True)
    first_name: Mapped[str] = mapped_column(default="")
    last_name: Mapped[str] = mapped_column(default="")
    birth_date: Mapped[datetime.date] = mapped_column(nullable=True)
    # role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum, name="role"), default=UserRoleEnum.BASIC)

    oauth_accounts = relationship("OAuthAccountModel", back_populates="profile", cascade="all, delete-orphan")

    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=partial(datetime.datetime.now, datetime.timezone.utc),
        onupdate=partial(datetime.datetime.now, datetime.timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Profile {self.email}>"
