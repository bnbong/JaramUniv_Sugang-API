# --------------------------------------------------------------------------
# Backend Application의 설정을 관리하는 파일입니다.
#
# 실제 환경에서는 .env 파일을 통해 설정을 관리하며,
# 테스트 환경에서는 .env.test 파일을 통해 설정을 관리합니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    DEBUG_MODE: bool = Field(
        default=True,
        description="If True, run the server in debug mode.",
    )
    LOGGING_DEBUG_LEVEL: bool = Field(
        default=True,
        description="True: DEBUG mode, False:: INFO mode",
    )
    ACCESS_LOG_FILE_PATH: str = Field(
        default="./logs/access.log",
        description="Log file path",
    )
    ERROR_LOG_FILE_PATH: str = Field(
        default="./logs/error.log",
        description="Error log file path",
    )
    DEBUG_ALLOW_CORS_ALL_ORIGIN: bool = Field(
        default=True,
        description="If True, allow origins for CORS requests.",
    )
    DEBUG_ALLOW_NON_CERTIFICATED_USER_GET_TOKEN: bool = Field(
        default=True,
        description="If True, allow non-cerficiated users to get ESP token.",
    )

    THREAD_POOL_SIZE: Optional[int] = Field(
        default=10,
        description="Change the server's thread pool size to handle non-async function",
    )

    SECRET_KEY: str = Field(
        default="example_secret_key_WoW",
        description="Secret key to be used for issuing HMAC tokens.",
    )

    DATABASE_URI: AnyUrl = Field(
        default="mysql+aiomysql://bnbong:password@localhost:3306/test",
        description="MariaDB connection URI.",
    )
    DATABASE_OPTIONS: Dict[str, Any] = Field(
        default={
            "pool_size": 10,
            "max_overflow": 20,
            "pool_recycle": 300,
            "pool_pre_ping": True,
        },
        description="MariaDB option to create a connection.",
    )

    model_config = SettingsConfigDict(env_file=".env")
