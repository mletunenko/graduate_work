from datetime import date, datetime

from pydantic import UUID4, BaseModel, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from utils.enums import UserRoleEnum
from utils.validators import validate_and_normalize_phone


class ProfileIn(BaseModel):
    email: EmailStr
    password: str
    phone: PhoneNumber
    first_name: str
    last_name: str
    birth_date: date
    role: UserRoleEnum = UserRoleEnum.BASIC

    @field_validator("phone")
    def validate_phone(cls, v):
        return validate_and_normalize_phone(v)


class ProfileOut(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    email: EmailStr
    phone: PhoneNumber
    first_name: str
    last_name: str
    birth_date: date
    role: str | None = None
