"""Module for settings class."""

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Base settings model."""

    DEBUG: bool = True
    ALPACA_API_KEY_ID: str
    ALPACA_SECRET_KEY: str


@lru_cache
def get_settings() -> Settings:
    """Generate settings."""
    return Settings()
