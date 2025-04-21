from datetime import date, datetime

from fastapi import Depends
from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from schemas.base import PaginationParams
from utils.validators import validate_and_normalize_phone


class ProfileIn(BaseModel):
    email: EmailStr
    password: str
    phone: PhoneNumber | None = None
    first_name: str = ""
    last_name: str = ""
    birth_date: date | None = None

    @field_validator("phone")
    def validate_phone(cls, v):
        return validate_and_normalize_phone(v)


class ProfileOut(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    email: EmailStr
    phone: PhoneNumber | None = None
    first_name: str = ""
    last_name: str = ""
    birth_date: date | None = None


class ProfileListParams(BaseModel):
    email: EmailStr | None = None
    birth_day: int | None = Field(None, description="День даты рождения", ge=1, le=31)
    birth_month: int | None = Field(None, description="Месяц даты рождения", ge=1, le=12)
    pagination: PaginationParams = Depends()


class ProfilePatch(BaseModel):
    phone: PhoneNumber | None = None
    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None

    @field_validator("phone")
    def validate_phone(cls, v):
        return validate_and_normalize_phone(v)


class UpdateEmailRequest(BaseModel):
    old_email: EmailStr
    new_email: EmailStr
