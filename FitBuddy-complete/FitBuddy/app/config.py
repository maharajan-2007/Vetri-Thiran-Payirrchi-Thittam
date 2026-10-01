from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FitBuddy – AI Fitness Plan Generator"
    database_url: str = "sqlite:///./fitbuddy.db"
    gemini_api_key: str | None = None
    workout_model: str = "gemini-2.5-pro"
    fast_model: str = "gemini-2.5-flash"
    admin_token: str = "change-me"
    max_age: int = 120
    min_age: int = 13
    max_weight_kg: float = 500
    min_weight_kg: float = 25

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
