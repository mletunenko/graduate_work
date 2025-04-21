from async_fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8006


class DatabaseConfig(BaseModel):
    url: str = "postgresql+asyncpg://user:password@127.0.0.1:30003/profiles"
    sync_url: str = "postgresql+psycopg://user:password@auth_postgres:30003/profiles"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class AuthServiceConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    create_user_path: str = "/auth/users"


class RabbitConfig(BaseModel):
    host: str = "localhost"
    login: str = "admin"
    password: str = "password"


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    authjwt_secret_key: str = "secret"
    algorithm: str = "HS256"
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    auth_service: AuthServiceConfig = AuthServiceConfig()
    rabbit: RabbitConfig = RabbitConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
