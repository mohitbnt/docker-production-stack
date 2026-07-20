"""Configuration classes for OpsPortal."""
import os
from datetime import timedelta


def _bool(v: str, default: bool = False) -> bool:
    if v is None:
        return default
    return str(v).lower() in ("1", "true", "yes", "on")


class BaseConfig:
    APP_NAME = os.getenv("APP_NAME", "OpsPortal")
    APP_ENV = os.getenv("APP_ENV", "production")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://opsportal:opsportal_pw@127.0.0.1:5432/opsportal",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
        "pool_size": 5,
        "max_overflow": 10,
    }

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-jwt")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_MINUTES", 15)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_TOKEN_DAYS", 7)))
    JWT_TOKEN_LOCATION = ["headers"]

    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    REDIS_CACHE_TTL_SECONDS = int(os.getenv("REDIS_CACHE_TTL_SECONDS", 60))

    CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]

    LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO").upper()
    LOG_DIR = os.getenv("APP_LOG_DIR", "/var/log/opsportal")

    SEED_ADMIN_EMAIL = os.getenv("SEED_ADMIN_EMAIL", "admin@opsportal.local")
    SEED_ADMIN_PASSWORD = os.getenv("SEED_ADMIN_PASSWORD", "Admin@12345")
    SEED_ADMIN_NAME = os.getenv("SEED_ADMIN_NAME", "System Administrator")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    APP_ENV = "development"


class ProductionConfig(BaseConfig):
    DEBUG = False
    APP_ENV = "production"


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", BaseConfig.SQLALCHEMY_DATABASE_URI)


def get_config():
    env = os.getenv("APP_ENV", "production").lower()
    return {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }.get(env, ProductionConfig)
