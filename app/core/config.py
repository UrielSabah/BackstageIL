from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = Field(..., description="PostgreSQL URL (e.g. Neon); sslmode=require is handled for asyncpg")
    SECRET_KEY: str = Field(..., min_length=1, description="API key for protected endpoints (e.g. X-API-Key)")

    # Pool tuning (defaults are fine for Neon serverless)
    DB_POOL_SIZE: int = Field(default=5, ge=1, le=20)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0, le=20)

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()