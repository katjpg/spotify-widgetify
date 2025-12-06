import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, Query, Request, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.config import get_settings, Settings
from app.utils.base64 import Base64Encoder
from app.api.spotify import SpotifyAuthClient, SpotifyApiClient
from app.domain.models import ThemeType, WidgetConfig
from app.domain.services import WidgetRenderingService
from app.themes import ThemeRegistry

logger = logging.getLogger(__name__)

# paths
BASE_PATH = Path(__file__).parent
STATIC_PATH = BASE_PATH / "static"
TEMPLATES_PATH = BASE_PATH / "templates"

# template mapping by theme
THEME_TEMPLATES: dict[ThemeType, str] = {
    ThemeType.IPOD: "ipod.html",
    ThemeType.VINYL: "vinyl.html",
    ThemeType.RETRO: "retro.html",
    ThemeType.WINDOWS98: "windows98.html",
    ThemeType.WINDOWSXP: "windowsxp.html",
    ThemeType.FRUTIGER_AERO: "frutiger_aero.html",
    ThemeType.MACINTOSH: "macintosh.html",
}

# singleton instances
_encoder: Base64Encoder | None = None
_auth_client: SpotifyAuthClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage shared HTTP client lifecycle."""
    app.state.http_client = httpx.AsyncClient(timeout=5.0)
    yield
    await app.state.http_client.aclose()


app = FastAPI(title="Spotify Widget", lifespan=lifespan)
templates = Jinja2Templates(directory=str(TEMPLATES_PATH))
app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")


# dependency injection
def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


def get_encoder() -> Base64Encoder:
    global _encoder
    if _encoder is None:
        _encoder = Base64Encoder(STATIC_PATH)
    return _encoder


def get_auth_client(
    settings: Settings = Depends(get_settings),
    http_client: httpx.AsyncClient = Depends(get_http_client)
) -> SpotifyAuthClient:
    global _auth_client
    if _auth_client is None:
        _auth_client = SpotifyAuthClient(settings, http_client)
    return _auth_client


def get_spotify_client(
    auth_client: SpotifyAuthClient = Depends(get_auth_client),
    settings: Settings = Depends(get_settings),
    encoder: Base64Encoder = Depends(get_encoder),
    http_client: httpx.AsyncClient = Depends(get_http_client)
) -> SpotifyApiClient:
    return SpotifyApiClient(auth_client, settings, encoder, http_client)


def get_rendering_service() -> WidgetRenderingService:
    return WidgetRenderingService()


def _get_template_name(theme: ThemeType, theme_data: dict[str, Any]) -> str:
    """Determine template based on theme type."""
    if "template_name" in theme_data:
        return theme_data["template_name"]
    return THEME_TEMPLATES.get(theme, "widget.html")


def _add_theme_context(
    context: dict[str, Any],
    theme: ThemeType
) -> None:
    """Add theme-specific context flags."""
    if theme == ThemeType.VINYL:
        context["spin"] = True
        context["use_vinyl_svg"] = True
    elif theme == ThemeType.RETRO:
        context["show_equalizer"] = True


async def _prepare_widget_data(
    request: Request,
    theme: str,
    style: str,
    color: str | None,
    eq_color: str,
    spotify_client: SpotifyApiClient,
    rendering_service: WidgetRenderingService,
    encoder: Base64Encoder,
    theme_type_legacy: str | None = None,
    theme_style_legacy: str | None = None,
) -> tuple[dict[str, Any], WidgetConfig, str]:
    """
    Prepare widget rendering data.

    Returns:
        Tuple of (context dict, config, template_name).
    """
    final_theme = theme_type_legacy or theme
    final_style = theme_style_legacy or style

    config = WidgetConfig.from_query_params(
        theme=final_theme,
        style=final_style,
        color=color,
        eq_color=eq_color
    )

    track = await spotify_client.get_current_track()

    base_data = rendering_service.prepare_rendering_data(
        track, config, encoder.get_spotify_logo()
    )

    # vinyl theme needs extra assets
    if config.theme == ThemeType.VINYL:
        base_data["vinyl_svg"] = encoder.get_vinyl_overlay()
        base_data["vinyl_needle_svg"] = encoder.get_vinyl_needle()

    theme_instance = ThemeRegistry.get_theme(config.theme, config.style, config.color)
    theme_data = theme_instance.transform_data(base_data)

    if "css" not in theme_data:
        theme_data["css"] = theme_instance.css

    context = {"request": request, **theme_data}
    _add_theme_context(context, config.theme)

    template_name = _get_template_name(config.theme, theme_data)

    return context, config, template_name


@app.get("/", response_class=HTMLResponse)
async def get_widget(
    request: Request,
    theme: str = Query("default"),
    style: str = Query("light"),
    color: str | None = Query(None, pattern=r"^[0-9A-Fa-f]{3,6}$"),
    eq_color: str = Query("1ED760"),
    spotify_client: SpotifyApiClient = Depends(get_spotify_client),
    rendering_service: WidgetRenderingService = Depends(get_rendering_service),
    encoder: Base64Encoder = Depends(get_encoder),
    theme_type: str | None = Query(None, include_in_schema=False),
    theme_style: str | None = Query(None, include_in_schema=False)
):
    context, config, template_name = await _prepare_widget_data(
        request, theme, style, color, eq_color,
        spotify_client, rendering_service, encoder,
        theme_type, theme_style
    )
    return templates.TemplateResponse(template_name, context)


@app.get("/github", response_class=Response)
async def get_github_image(
    request: Request,
    theme: str = Query("default"),
    style: str = Query("light"),
    color: str | None = Query(None, pattern=r"^[0-9A-Fa-f]{3,6}$"),
    eq_color: str = Query("1ED760"),
    spotify_client: SpotifyApiClient = Depends(get_spotify_client),
    rendering_service: WidgetRenderingService = Depends(get_rendering_service),
    encoder: Base64Encoder = Depends(get_encoder),
    theme_type: str | None = Query(None, include_in_schema=False),
    theme_style: str | None = Query(None, include_in_schema=False)
):
    context, config, template_name = await _prepare_widget_data(
        request, theme, style, color, eq_color,
        spotify_client, rendering_service, encoder,
        theme_type, theme_style
    )

    content = templates.get_template(template_name).render(context)
    # fix XML entity encoding
    content = content.replace("&", "&amp;").replace("&amp;amp;", "&amp;")

    return Response(content=content, media_type="image/svg+xml")


@app.get("/link", response_class=HTMLResponse)
async def get_link_page(
    request: Request,
    spotify_client: SpotifyApiClient = Depends(get_spotify_client)
):
    track = await spotify_client.get_current_track()
    embed_link = f"https://open.spotify.com/embed/track/{track.id}"

    return templates.TemplateResponse(
        "link.html",
        {"request": request, "embed_link": embed_link}
    )
