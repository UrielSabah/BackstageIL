from pydantic import  Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DB_URL: str

    SECRET_KEY: str

    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    REGION_NAME: str = Field(default="eu-north-1")
    BUCKET_NAME: str
    AWS_USER_NAME: str
    AWS_REGION: str

    class Config:
        env_file = ".env"   # automatically load from .env
        env_file_encoding = "utf-8"

settings = Settings()