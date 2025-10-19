# app/config.py
from pydantic_settings import BaseSettings
from pydantic import HttpUrl

class Settings(BaseSettings):
    redis_url: str = "redis://redis:6379/0"
    internal_api_1: HttpUrl = "http://internal-api-1.local/endpoint"
    internal_api_2: HttpUrl = "http://internal-api-2.local/endpoint"

    class Config:
        env_file = ".env"

settings = Settings()