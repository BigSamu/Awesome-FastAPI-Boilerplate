from typing import ClassVar

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # PATH SETTINGS
    API_V1_STR: str = "/api/v1"  # Prefix URL for API version
    BASE_PATH: ClassVar[Path]  = (
        Path(__file__).resolve().parent.parent
    )  # Base Path for accessing SEG-Y file

    # JWT SETTINGS
    # JWT_SECRET_KEY: str = secrets.token_urlsafe(32)  # Generate by server randomly
    JWT_SECRET_KEY: str = "my secret"
    JWT_SIGN_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 1 day

    # DATABASE SETTINGS
    DATABASE_URL: str = "sqlite:///./mini-blog.db"  # Database Location

    ARTS_API_URL: str = "http://localhost:8080"

    class Config:
        env_file = ".env"


settings = Settings()
