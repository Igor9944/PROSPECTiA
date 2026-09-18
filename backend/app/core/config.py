from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)

    PROJECT_NAME: str = "PROSPECTIA"
    API_PREFIX: str = "/api"

    SECRET_KEY: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    DATABASE_URL: str = "sqlite:///./prospection.db"
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://localhost:5173,http://localhost:4173,"
        "https://igor9944.github.io"
    )

    AI_PROVIDER: str = "none"
    AI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    SEED_ON_START: bool = False

    @field_validator("DATABASE_URL")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgres://"):
            return "postgresql://" + value[len("postgres://") :]
        return value

    @property
    def ai_api_key(self) -> str:
        return self.AI_API_KEY or self.GEMINI_API_KEY

    @property
    def cors_origin_list(self) -> list[str]:
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        if "*" in origins:
            return ["*"]
        return origins


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
