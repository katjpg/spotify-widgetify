from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Spotify credentials and API endpoints, read from SPOTIFY_-prefixed env vars (or .env)."""

    model_config = SettingsConfigDict(
        env_prefix="SPOTIFY_",  # reads SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, ...
        env_file=".env",  # local only; the host injects real env vars
        env_file_encoding="utf-8",
        extra="ignore",
    )

    client_id: str = ""
    client_secret: SecretStr = SecretStr("")
    refresh_token: SecretStr = SecretStr("")

    spotify_api_url: str = "https://api.spotify.com/v1"
    auth_api_url: str = "https://accounts.spotify.com/api/token"


@lru_cache
def get_settings() -> Settings:
    return Settings()
