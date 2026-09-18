from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=True)

    PROJECT_NAME: str = "PROSPECTIA"
    API_PREFIX: str = "/api"

    SECRET_KEY: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    DATABASE_URL: str = "sqlite:////home/ro0t_h4ck/PROSPECTIA/backend/prospection.db"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    AI_PROVIDER: str = "none"
    AI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    @property
    def ai_api_key(self) -> str:
        return self.AI_API_KEY or self.GEMINI_API_KEY

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
