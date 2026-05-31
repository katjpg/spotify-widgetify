from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.assets.images import ImageEncoder
from app.config import get_settings
from app.providers.spotify import SpotifyAuthClient

BASE_PATH = Path(__file__).resolve().parent
STATIC_PATH = BASE_PATH / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=5.0)
    app.state.encoder = ImageEncoder(STATIC_PATH)
    app.state.auth_client = SpotifyAuthClient(get_settings(), app.state.http_client)
    yield
    await app.state.http_client.aclose()


app = FastAPI(title="Spotify Widget", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")
app.include_router(router)
