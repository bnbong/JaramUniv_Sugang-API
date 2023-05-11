from __future__ import annotations

from pydantic import BaseSettings, Field


class Settings(BaseSettings):

    DB_URI: str = Field(
        default="mysql+aiomysql://jaramhubuser:jaramhubpassword@localhost:3306/jhubsugang",
        description="MariaDB URI",
    )

    class Config:
        env_file = ".env"
