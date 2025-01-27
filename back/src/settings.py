"""Configuration settings for the URL shortener service."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration."""

    # Redis settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_USERNAME: str = "default"
    REDIS_DB: int = 0

    # CORS settings
    CORS_ORIGINS: str = "http://localhost:3000"

    # Base URL for shortened links
    BASE_URL: str = "http://localhost:8000/"

    @property
    def REDIS_URL(self) -> str:
        """Generate Redis URL from components."""
        auth_part = (
            f"{self.REDIS_USERNAME}:{self.REDIS_PASSWORD}@"
            if self.REDIS_PASSWORD
            else ""
        )
        return f"redis://{auth_part}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    class Config:
        """Pydantic configuration class."""

        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
