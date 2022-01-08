"""Module for settings class."""

from functools import lru_cache

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """Base settings model."""

    DEBUG: bool = True
    ALPACA_API_KEY_ID: SecretStr
    ALPACA_SECRET_KEY: SecretStr


@lru_cache
def get_settings() -> Settings:
    """Generate settings."""
    return Settings()
