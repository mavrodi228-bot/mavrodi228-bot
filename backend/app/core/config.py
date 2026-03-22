from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'CashLens API'
    api_prefix: str = '/api'
    environment: str = 'development'
    debug: bool = True

    database_url: str = Field(
        default='postgresql+psycopg://cashlens:cashlens@db:5432/cashlens'
    )
    demo_mode: bool = True
    encryption_key: str = Field(default='u4O5jL0_hKjXr7o25W8dR7P7sT9xYlR8vQ1cZx2AsQ8=')

    tbank_business_base_url: str = 'https://business.tbank.ru/openapi'
    tbank_business_token: str = ''
    tbank_business_account_id: str = ''
    tbank_business_company_id: str = ''
    tbank_business_timeout_seconds: int = 20

    cors_origins: list[str] = ['http://localhost:5173']

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
