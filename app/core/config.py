"""
This file manages the configuration of the application.
"""

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Configuration for JWT and environment variables.
    """

    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    class Config:
        """
        Settings for Pydantic environment file.
        """

        # pylint: disable=too-few-public-methods

        env_file = ".env"


settings = Settings()
