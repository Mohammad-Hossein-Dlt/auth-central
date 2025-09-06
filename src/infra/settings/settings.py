from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BASE_URL: str
    AUTH_DB_STACK: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
        
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings: Settings = Settings()
