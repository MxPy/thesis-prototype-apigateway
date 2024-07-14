import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #TODO: move to env
    USERS_SERVICE_URL: str = "http://localhost:8000"
    GATEWAY_TIMEOUT: int = 59


settings = Settings()