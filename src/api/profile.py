from fastapi import APIRouter, Depends, Response
from pydantic import UUID4
from starlette.status import HTTP_204_NO_CONTENT

from db.postgres import SessionDep
from models import ProfileModel
from schemas.profile import ProfileIn, ProfileListParams, ProfileOut, ProfilePatch
from services.profile import ProfileService

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("", summary="Создать профиль пользователя", response_model=ProfileOut)
async def create_profile(data: ProfileIn, session: SessionDep) -> ProfileModel:
    profile = await ProfileService.create_profile(data, session)
    return profile


@router.get("", summary="Получить список профилей", response_model=list[ProfileOut])
async def list_profile(session: SessionDep, query_params: ProfileListParams = Depends()) -> list[ProfileModel]:
    profiles_list = await ProfileService.get_profile_list(session, query_params)
    return profiles_list


@router.get("/{profile_id}", summary="Получить профиль по id", response_model=ProfileOut)
async def get_profile_by_id(profile_id: UUID4, session: SessionDep) -> ProfileModel:
    profile = await ProfileService.get_profile_by_id(profile_id, session)
    return profile


@router.patch("/{profile_id}", summary="Обновить профиль пользователя", response_model=ProfileOut)
async def update_profile(
    profile_id: UUID4,
    data: ProfilePatch,
    session: SessionDep,
) -> ProfileModel:
    profile = await ProfileService.update_profile(profile_id, data, session)
    return profile


@router.delete("/{profile_id}", summary="Удалить профиль пользователя")
async def delete_profile(profile_id: UUID4, session: SessionDep) -> Response:
    await ProfileService.delete_profile(profile_id, session)
    return Response(status_code=HTTP_204_NO_CONTENT)
