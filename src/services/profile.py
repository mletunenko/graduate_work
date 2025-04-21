from fastapi import HTTPException
from pydantic import EmailStr
from pydantic.v1 import UUID4
from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from models import ProfileModel
from schemas.profile import ProfileIn, ProfileListParams, ProfilePatch
from utils.enums import ClientErrorMessage


class ProfileService:
    @staticmethod
    async def get_profile_by_email(email: EmailStr, session: AsyncSession) -> ProfileModel | None:
        stmt = select(ProfileModel).where(ProfileModel.email == email)
        result = await session.execute(stmt)
        profile = result.scalars().first()
        return profile

    @staticmethod
    async def get_profile_by_phone(phone: str, session: AsyncSession) -> ProfileModel | None:
        stmt = select(ProfileModel).where(ProfileModel.phone == phone)
        result = await session.execute(stmt)
        profile = result.scalars().first()
        return profile

    @staticmethod
    async def create_profile(
        data: ProfileIn,
        session: AsyncSession,
    ) -> ProfileModel:
        if await ProfileService.get_profile_by_email(data.email, session):
            raise HTTPException(status_code=400, detail=ClientErrorMessage.NOT_UNIQUE_EMAIL_ERROR.value)
        if data.phone and await ProfileService.get_profile_by_phone(data.phone, session):
            raise HTTPException(status_code=400, detail=ClientErrorMessage.NOT_UNIQUE_PHONE_ERROR.value)

        profile = ProfileModel(
            email=data.email,
            phone=data.phone,
            first_name=data.first_name,
            last_name=data.last_name,
            birth_date=data.birth_date,
        )
        session.add(profile)
        await session.commit()
        return profile

    @staticmethod
    async def get_profile_by_id(profile_id: UUID4, session: AsyncSession) -> ProfileModel:
        stmt = select(ProfileModel).where(ProfileModel.id == profile_id)
        result = await session.execute(stmt)
        profile = result.scalars().first()
        if not profile:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=ClientErrorMessage.NOT_FOUND_PROFILE_ERROR.value)
        return profile

    @staticmethod
    async def delete_profile(profile_id: UUID4, session: AsyncSession) -> None:
        profile = await ProfileService.get_profile_by_id(profile_id, session)
        await session.delete(profile)
        await session.commit()

    @staticmethod
    async def update_profile(profile_id: UUID4, data: ProfilePatch, session: AsyncSession) -> ProfileModel:
        profile = await ProfileService.get_profile_by_id(profile_id, session)
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
        await session.commit()
        return profile

    @staticmethod
    async def get_profile_list(session: AsyncSession, query_params: ProfileListParams) -> list[ProfileModel]:
        stmt = select(ProfileModel)
        if query_params.birth_day:
            stmt = stmt.filter(extract("day", ProfileModel.birth_date) == query_params.birth_day)
        if query_params.birth_month:
            stmt = stmt.filter(extract("month", ProfileModel.birth_date) == query_params.birth_month)
        if query_params.email:
            stmt = stmt.filter(ProfileModel.email == query_params.email)
        stmt = stmt.offset((query_params.pagination.page_number - 1) * query_params.pagination.page_size).limit(
            query_params.pagination.page_size
        )

        result = await session.execute(stmt)
        profile_list = list(result.scalars().all())
        return profile_list

    @staticmethod
    async def is_phone_unique(
        new_phone: str,
        profile_id: UUID4,
        session: AsyncSession,
    ) -> bool:
        stmt = select(ProfileModel).where(ProfileModel.id != profile_id).where(ProfileModel.phone == new_phone)
        result = await session.execute(stmt)
        existent_profile = result.scalars().first()
        if existent_profile:
            return False
        return True
