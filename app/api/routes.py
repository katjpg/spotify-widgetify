import html
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_rendering_service, get_spotify_client
from app.providers.spotify import SpotifyClient
from app.schemas.widget import WidgetParams, build_config
from app.services.rendering import RenderingService

TEMPLATES_PATH = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_PATH))

router = APIRouter()


@router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    # embed service has no browseable site; answer the browser's automatic request without a 404
    return Response(status_code=204)


@router.get("/", response_class=HTMLResponse)
async def get_widget(
    request: Request,
    params: Annotated[WidgetParams, Query()],
    spotify: SpotifyClient = Depends(get_spotify_client),
    rendering: RenderingService = Depends(get_rendering_service),
) -> Response:
    config = build_config(params)
    track = await spotify.fetch_current_track()
    rendered = rendering.render_widget(track, config)
    return templates.TemplateResponse(request, rendered.template_name, rendered.context)


@router.get("/github", response_class=Response)
async def get_github_image(
    request: Request,
    params: Annotated[WidgetParams, Query()],
    spotify: SpotifyClient = Depends(get_spotify_client),
    rendering: RenderingService = Depends(get_rendering_service),
) -> Response:
    config = build_config(params)
    track = await spotify.fetch_current_track()
    rendered = rendering.render_widget(track, config)

    content = templates.get_template(rendered.template_name).render(
        {"request": request, **rendered.context}
    )
    # decode HTML entities (&#39; -> '), then re-encode bare & so the SVG is valid XML
    content = html.unescape(content)
    content = content.replace("&", "&amp;")
    return Response(content=content, media_type="image/svg+xml")


@router.get("/link", response_class=HTMLResponse)
async def get_link_page(
    request: Request,
    spotify: SpotifyClient = Depends(get_spotify_client),
) -> Response:
    track = await spotify.fetch_current_track()
    embed_link = f"https://open.spotify.com/embed/track/{track.track_id}"
    return templates.TemplateResponse(request, "link.html", {"embed_link": embed_link})
