import httpx
from fastapi import Depends, Request

from app.assets.images import ImageEncoder
from app.config import Settings, get_settings
from app.providers.spotify import SpotifyAuthClient, SpotifyClient
from app.services.rendering import RenderingService


def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


def get_encoder(request: Request) -> ImageEncoder:
    return request.app.state.encoder


def get_auth_client(request: Request) -> SpotifyAuthClient:
    return request.app.state.auth_client


def get_spotify_client(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> SpotifyClient:
    state = request.app.state
    return SpotifyClient(state.auth_client, settings, state.encoder, state.http_client)


def get_rendering_service(request: Request) -> RenderingService:
    return RenderingService(request.app.state.encoder)
