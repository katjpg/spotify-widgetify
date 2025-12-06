from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    client_id: str = Field(default="", alias="CLIENT_ID")
    client_secret: str = Field(default="", alias="CLIENT_SECRET")
    refresh_token: str = Field(default="", alias="REFRESH_TOKEN")

    spotify_api_url: str = "https://api.spotify.com/v1"
    auth_api_url: str = "https://accounts.spotify.com/api/token"
    default_eq_color: str = "1ED760"

    @field_validator('default_eq_color')
    @classmethod
    def validate_hex_color(cls, v: str) -> str:
        v = v.lstrip('#')
        if len(v) not in (3, 6) or not all(c in '0123456789ABCDEFabcdef' for c in v):
            raise ValueError('Invalid hex color format')
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
