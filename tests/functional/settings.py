from pydantic_settings import BaseSettings, SettingsConfigDict

from .utils.get_env_path import detect_env_file


env_path = detect_env_file('.env', '../..')


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
