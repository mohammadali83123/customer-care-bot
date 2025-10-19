# app/config.py
from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    redis_url: str = "redis://redis:6379/0"
    internal_api_1: AnyUrl = "http://internal-api-1.local/endpoint"
    internal_api_2: AnyUrl = "http://internal-api-2.local/endpoint"

    class Config:
        env_file = ".env"

settings = Settings()