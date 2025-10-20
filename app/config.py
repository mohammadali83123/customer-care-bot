# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    redis_url: str = "redis://redis:6379/0"
    internal_api_1: HttpUrl = os.getenv("CHECK_CUSTOMER_REGISTRATION_API_URL")
    internal_api_2: HttpUrl = "http://internal-api-2.local/endpoint"

    access_token: str = os.getenv("ACCESS_TOKEN")

settings = Settings()