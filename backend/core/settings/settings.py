from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='backend/.env', extra='ignore')
    postgres_user: str
    postgres_password: str
    postgres_db: str
    secret_key: str
    access_token_encrypt_algorithm: str
    access_token_expires_minutes: int

    @property
    def url(self) -> str:
        return (f"postgresql+asyncpg:"
                f"//{self.postgres_user}:{self.postgres_password}"
                f"@0.0.0.0:5433/{self.postgres_db}")


@lru_cache
def get_settings() -> Settings:
    return Settings()
