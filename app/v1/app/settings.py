from __future__ import annotations

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class Settings(BaseSettings):

    DB_URI: str = Field(
        default="",
        description="MariaDB URI",
    )

    class Config:
        env_file = ".env"
