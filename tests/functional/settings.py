import asyncio

from pydantic_settings import BaseSettings, SettingsConfigDict

from .utils.detect_file import get_file_path


env_path = asyncio.run(get_file_path('.env', '../..'))


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='allow', env_file=env_path)

    es_host: str
    es_port: int
    movies_index_name: str
    persons_index_name: str
    movies_index_file: str
    persons_index_file: str

    redis_host: str
    redis_port: str

    service_url: str


test_settings = TestSettings()
