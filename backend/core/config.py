import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 9010
    RELEASE_VERSION: str = "1.0.0"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24
    SECRET_KEY: str = "super-secret-key"


class DevelopmentConfig(Config):
    MARIADB_URL: str = "mariadb+pymysql://user:password@127.0.0.1:5432/urlslab-bot"


class ProductionConfig(Config):
    ENV: str = "prod"
    DEBUG: bool = False
    MARIADB_URL: str = "mariadb+pymysql://user:password@127.0.0.1:5432/urlslab-bot"


def get_config():
    env = os.getenv("ENV", "dev")
    config_type = {
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
