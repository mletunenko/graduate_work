from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import UUID4
from redis.asyncio import Redis
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)

from db.postgres import SessionDep
from db.rabbit import RabbitDep
from db.redis import get_redis_connection
from models import ProfileModel
from schemas.profile import ProfileIn, ProfileListParams, ProfileOut, ProfilePatch
from services.profile import ProfileService
from sync.tasks import create_user_task, delete_user_task
from utils.enums import ClientErrorMessage
from utils.token import check_invalid_token

router = APIRouter(prefix="/profiles", tags=["profile"])
auth_bearer = AuthJWTBearer()


@router.post("", summary="Создать профиль пользователя", response_model=ProfileOut)
async def create_profile(
    data: ProfileIn,
    session: SessionDep,
    rabbit_channel: RabbitDep,
) -> ProfileModel:
    profile = await ProfileService.create_profile(data, session)
    await create_user_task(data, rabbit_channel)
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
    authorize: AuthJWT = Depends(auth_bearer),
    redis: Redis = Depends(get_redis_connection),
) -> ProfileModel:
    await authorize.jwt_required()
    token = await authorize.get_raw_jwt()
    if await check_invalid_token(token, redis):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token invalid")
    profile = await ProfileService.get_profile_by_id(profile_id, session)
    if profile.email != token["email"]:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token invalid")

    if data.phone and not await ProfileService.is_phone_unique(data.phone, profile_id, session):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=ClientErrorMessage.NOT_UNIQUE_PHONE_ERROR.value,
        )

    profile = await ProfileService.update_profile(profile_id, data, session)
    return profile


@router.delete("/{profile_id}", summary="Удалить профиль пользователя")
async def delete_profile(
    profile_id: UUID4,
    session: SessionDep,
    rabbit_channel: RabbitDep,
    authorize: AuthJWT = Depends(auth_bearer),
    redis: Redis = Depends(get_redis_connection),
) -> Response:
    await authorize.jwt_required()
    token = await authorize.get_raw_jwt()
    if await check_invalid_token(token, redis):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token invalid")
    profile = await ProfileService.get_profile_by_id(profile_id, session)
    if profile.email != token["email"]:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token invalid")

    profile = await ProfileService.get_profile_by_id(profile_id, session)
    await ProfileService.delete_profile(profile_id, session)
    await delete_user_task(profile, rabbit_channel)
    return Response(status_code=HTTP_204_NO_CONTENT)
