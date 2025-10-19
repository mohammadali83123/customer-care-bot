# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    redis_url: str = "redis://redis:6379/0"
    internal_api_1: HttpUrl = "http://internal-api-1.local/endpoint"
    internal_api_2: HttpUrl = "http://internal-api-2.local/endpoint"

settings = Settings()