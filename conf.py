import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #TODO: move to env
    #change users to localhost for nondocker run
    AUTH_SERVICE_URL: str = "http://users:8000"
    AUTH_SERVICE_GRPC : str = "users:50051"
    SENSORS_SERVICE_URL: str = "http://sensor-py-service:8000"
    HEALTH_SERVICE_URL: str = "http://user-node-service:3002"
    MOCK_SERVICE_URL: str = "http://mock:8000"
    GATEWAY_TIMEOUT: int = 59
    ACCESS_TOKEN_DEFAULT_EXPIRE_MINUTES: int = 360


settings = Settings()