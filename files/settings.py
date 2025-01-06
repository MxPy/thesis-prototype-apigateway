from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MINIO_ROOT_USER: str = "username"
    MINIO_ROOT_PASSWORD: str = "password"
    MINIO_HOST: str = "minio"
    MINIO_PORT: int = 9000
    MINIO_SECURE: bool = False
    MINIO_URI: str = f'{MINIO_HOST}:{MINIO_PORT}'
    MINIO_PUBLIC_URL: str = f'localhost:{MINIO_PORT}'
    ACCESS_KEY: str = "bnCFFeQLdQP5yljquLmR"
    SECRET_KEY: str = "zfW6JYVW5wsjBMEpAw7cda0sGwU4wdJTz2K5Z98W"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()