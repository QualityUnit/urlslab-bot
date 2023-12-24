import os
from typing import Optional

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
    MARIADB_URL: str = "mariadb+pymysql://user:password@127.0.0.1:5432/urlslab-bot"
    QDRANT_URL: str = "http://localhost:6333"
    REDIS_URL: str = "redis://localhost:6379"


class DevelopmentConfig(Config):
    model_config = SettingsConfigDict(env_file='.env.dev', env_file_encoding='utf-8')


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
