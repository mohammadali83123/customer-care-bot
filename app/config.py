# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    REDIS_URL: str = ""
    CHECK_CUSTOMER_REGISTRATION_API_URL: HttpUrl
    FETCH_CUSTOMER_ORDERS_API_URL: HttpUrl

    ACCESS_TOKEN: str = ""

settings = Settings()