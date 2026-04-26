from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'ai-callcenter'
    environment: str = 'development'
    api_prefix: str = '/api/v1'
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14

    database_url: str
    redis_url: str

    openai_api_key: str
    openai_realtime_model: str = 'gpt-4o-mini-realtime-preview'

    s3_endpoint: str
    s3_bucket: str
    s3_access_key: str
    s3_secret_key: str

    log_level: str = 'INFO'


settings = Settings()
