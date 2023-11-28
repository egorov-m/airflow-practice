from enum import Enum
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class EnvironmentType(str, Enum):
    DEV = "DEV"
    LOCAL = "LOCAL"
    PROD = "PROD"


class Settings(BaseSettings):
    PROJECT_NAME: str = "fake_data_generator"
    VERSION: str = "0.0.1"
    LOG_FILENAME: str = "log"
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEV
    DEBUG: bool = True

    SQL_SCHEMA: str = "postgresql"
    DB_DRIVER: str = "asyncpg"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_SSL: str = "prefer"  # disable, allow, prefer, require, verify-ca, verify-full
    DB_USER: str = "airflow"
    DB_PASSWORD: str = "airflow"
    DB_NAME: str = "fake_db"

    DB_POOL_SIZE: int = 75
    DB_MAX_OVERFLOW: int = 20

    def get_db_url(self):
        return (f"{self.SQL_SCHEMA}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?ssl={self.DB_SSL}")

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
