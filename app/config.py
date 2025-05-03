from pydantic import Field, BaseModel
import os
from functools import lru_cache
from dotenv import load_dotenv

# load environment variables
load_dotenv()


class Settings(BaseModel):
    """application settings"""
    # api credentials
    client_id: str = Field(default_factory=lambda: os.getenv("CLIENT_ID", ""))
    client_secret: str = Field(default_factory=lambda: os.getenv("CLIENT_SECRET", ""))
    refresh_token: str = Field(default_factory=lambda: os.getenv("REFRESH_TOKEN", ""))
    
    # api endpoints
    spotify_api_url: str = "https://api.spotify.com/v1"
    auth_api_url: str = "https://accounts.spotify.com/api/token"
    
    # defaults
    default_eq_color: str = "1ED760"


@lru_cache
def get_settings() -> Settings:
    """provide cached settings instance"""
    return Settings()