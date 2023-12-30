import os
from typing import Optional

from langchain.globals import set_verbose
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 9010
    RELEASE_VERSION: str = "1.0.0"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24
    SECRET_KEY: str = "super-secret-key"
    MARIADB_URL: str = "mariadb+asyncmy://user:password@127.0.0.1:5432/urlslab-bot"
    QDRANT_URL: str = "http://localhost:6333"
    REDIS_URL: str = "redis://localhost:6379"
    QDRANT_COLLECTION_NAME: str = "urlslab_bot"
    REDIS_EMBEDDING_MODEL_KEY: str = "urlslab_bot_embedding_model"
    DEFAULT_EMBEDDING_MODEL_CLASS: str = "FastEmbedEmbeddings"
    DEFAULT_EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en"
    VERSION_KEY: str = "urlslab_bot_version"
    API_KEY: str = "dev-key"


class DevelopmentConfig(Config):
    model_config = SettingsConfigDict(env_file='.env.dev', env_file_encoding='utf-8')

    # Setting verbose for langchain
    set_verbose(True)


class ProductionConfig(Config):
    ENV: str = "prod"
    DEBUG: bool = False
    model_config = SettingsConfigDict(env_file='.env.prod', env_file_encoding='utf-8')


def get_config():
    env = os.getenv("ENV", "dev")
    config_type = {
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
