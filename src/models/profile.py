import datetime

from pydantic import UUID4
from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Profile(Base):
    __tablename__ = "profiles"
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(default="")
    last_name: Mapped[str] = mapped_column(default="")
    birth_date: Mapped[datetime.date] = mapped_column()

    role_id: Mapped[UUID4 | None] = mapped_column(ForeignKey("roles.id", ondelete="SET NULL"))
    role: Mapped["Role"] = relationship(lazy="joined")

    oauth_accounts = relationship("OAuthAccount", back_populates="profile", cascade="all, delete-orphan")

    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Profile {self.email}>"


class Role(Base):
    __tablename__ = "roles"

    title: Mapped[str] = mapped_column(unique=True)
    system_role: Mapped[bool | None] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"<Role {self.title}>"
