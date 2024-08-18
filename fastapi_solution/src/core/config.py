from logging import config as logging_config
from pathlib import Path

from .logger import LOGGING
from pydantic_settings import BaseSettings, SettingsConfigDict

logging_config.dictConfig(LOGGING)


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR.joinpath(".env"), case_sensitive=True, extra="allow")

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: int
    
    # ELASTIC
    ELASTIC_HOST: str
    ELASTIC_PORT: int

    # PROJECT
    PROJECT_NAME: str

    # RETRY POLICY
    MAX_TRIES: int = 10


settings = Settings()