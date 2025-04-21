import uuid

import backoff
from async_fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException
from redis.asyncio import Redis
from redis.exceptions import ConnectionError
from starlette.status import HTTP_401_UNAUTHORIZED


@backoff.on_exception(backoff.expo, ConnectionError, max_time=15)
async def check_invalid_token(
    token: dict,
    redis: Redis,
) -> bool:
    jti = token["jti"]
    res = await redis.get(f"blacklist:{jti}")
    return res


async def get_user_id_from_token(authorize: AuthJWT, redis: Redis) -> uuid.UUID:
    try:
        await authorize.jwt_required()
        token = await authorize.get_raw_jwt()
        if await check_invalid_token(token, redis):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token invalid")

        user_id = await authorize.get_jwt_subject()
        user_uuid = uuid.UUID(user_id)
        return user_uuid
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token invalid")
