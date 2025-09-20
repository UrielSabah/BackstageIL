# from dotenv import load_dotenv
# import os

# load_dotenv()
# DB_URL = os.getenv("DB_URL")
# SECRET_KEY = os.getenv("SECRET_KEY")
#
# # AWS
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# REGION_NAME = os.getenv('AWS_REGION', 'eu-north-1')  # Default region
# BUCKET_NAME = os.getenv('BUCKET_NAME')
from pydantic import  Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DB_URL: str

    # App secrets
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