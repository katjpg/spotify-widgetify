from fastapi import FastAPI, Query, Request, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional

from app.config import get_settings, Settings
from app.utils.base64 import Base64Encoder
from app.api.spotify import SpotifyAuthClient, SpotifyApiClient
from app.domain.models import ThemeStyle, ThemeType, WidgetConfig
from app.domain.services import VisualizationService, WidgetRenderingService
from app.themes import ThemeRegistry


# initialize app
app = FastAPI(title="Spotify Widget")

# set up directories
BASE_PATH = Path(__file__).parent
STATIC_PATH = BASE_PATH / "static"
TEMPLATES_PATH = BASE_PATH / "templates"

# set up static and templates
templates = Jinja2Templates(directory=str(TEMPLATES_PATH))
app.mount("/static", StaticFiles(directory=str(STATIC_PATH)), name="static")


# dependency injection container
def get_encoder() -> Base64Encoder:
    """provide base64 encoder instance"""
    return Base64Encoder(STATIC_PATH)


def get_auth_client(settings: Settings = Depends(get_settings)) -> SpotifyAuthClient:
    """provide spotify auth client"""
    return SpotifyAuthClient(settings)


def get_spotify_client(
    auth_client: SpotifyAuthClient = Depends(get_auth_client),
    settings: Settings = Depends(get_settings),
    encoder: Base64Encoder = Depends(get_encoder)
) -> SpotifyApiClient:
    """provide spotify api client"""
    return SpotifyApiClient(auth_client, settings, encoder)


def get_visualization_service() -> VisualizationService:
    """provide visualization service"""
    return VisualizationService()


def get_rendering_service(
    visualization: VisualizationService = Depends(get_visualization_service)
) -> WidgetRenderingService:
    """provide widget rendering service"""
    return WidgetRenderingService(visualization)


@app.get("/", response_class=HTMLResponse)
async def get_widget(
    request: Request,
    theme: str = Query("default", description="Theme (default/vinyl/ipod/retro/windows98)"),
    style: str = Query("light", description="Style (light/dark)"),
    color: Optional[str] = Query(None, description="HEX color code (only for ipod, vinyl, and default)"),
    eq_color: str = Query("1ED760", description="Equalizer color (HEX without # or 'rainbow' or 'none')"),
    spotify_client: SpotifyApiClient = Depends(get_spotify_client),
    rendering_service: WidgetRenderingService = Depends(get_rendering_service),
    encoder: Base64Encoder = Depends(get_encoder),
    # support for old parameter names
    theme_type: Optional[str] = Query(None, include_in_schema=False),
    theme_style: Optional[str] = Query(None, include_in_schema=False)
):
    """generate spotify widget svg"""
    # use old parameter names if provided
    final_theme = theme_type or theme
    final_style = theme_style or style
    
    print(f"Request params - theme: {final_theme}, style: {final_style}, color: {color}")
    
    # create widget configuration with parameters
    config = WidgetConfig.from_query_params(
        theme=final_theme, 
        style=final_style, 
        color=color,
        eq_color=eq_color
    )
    
    # get data from spotify
    track = await spotify_client.get_current_track()
    
    # prepare base rendering data
    base_data = rendering_service.prepare_rendering_data(
        track, config, encoder.get_spotify_logo()
    )
    
    # add theme-specific assets
    if config.theme == ThemeType.VINYL:
        base_data["vinyl_svg"] = encoder.get_vinyl_overlay()
        base_data["vinyl_needle_svg"] = encoder.get_vinyl_needle()
    
    # apply theme-specific transformations
    theme_instance = ThemeRegistry.get_theme(config.theme, config.style, config.color)
    theme_data = theme_instance.transform_data(base_data)
    
    # ensure css variable is properly passed
    if "css" not in theme_data:
        theme_data["css"] = theme_instance.css
        
    # debug info
    print(f"Background color after theme processing: {theme_data['css'].get('background_color')}")
    
    # add request to context
    context = {"request": request, **theme_data}
    
    # select appropriate template based on theme
    template_name = "widget.html"  # default
    
    if config.theme == ThemeType.IPOD:
        template_name = "ipod.html"
    elif config.theme == ThemeType.VINYL:
        template_name = "vinyl.html"
        context["spin"] = True
        context["use_vinyl_svg"] = True
    elif config.theme == ThemeType.RETRO:
        template_name = "retro.html"
        context["show_equalizer"] = True
    elif config.theme == ThemeType.WINDOWS98:
        template_name = "windows98.html"
    
    # override with theme-specific template if provided
    if "template_name" in theme_data:
        template_name = theme_data["template_name"]
    
    return templates.TemplateResponse(template_name, context)


@app.get("/github", response_class=Response)
async def get_github_image(
    request: Request,
    theme: str = Query("default", description="Theme (default/vinyl/ipod/retro/windows98)"),
    style: str = Query("light", description="Style (light/dark)"),
    color: Optional[str] = Query(None, description="HEX color code (only for ipod, vinyl, and default)"),
    eq_color: str = Query("1ED760", description="Equalizer color (HEX without # or 'rainbow' or 'none')"),
    spotify_client: SpotifyApiClient = Depends(get_spotify_client),
    rendering_service: WidgetRenderingService = Depends(get_rendering_service),
    encoder: Base64Encoder = Depends(get_encoder),
    theme_type: Optional[str] = Query(None, include_in_schema=False),
    theme_style: Optional[str] = Query(None, include_in_schema=False)
):
    """generate github-friendly image"""
    # use old parameter names if provided
    final_theme = theme_type or theme
    final_style = theme_style or style
    
    # create widget configuration with parameters
    config = WidgetConfig.from_query_params(
        theme=final_theme, 
        style=final_style, 
        color=color,
        eq_color=eq_color
    )
    
    # get data from spotify
    track = await spotify_client.get_current_track()
    
    # prepare base rendering data
    base_data = rendering_service.prepare_rendering_data(
        track, config, encoder.get_spotify_logo()
    )
    
    # add theme-specific assets
    if config.theme == ThemeType.VINYL:
        base_data["vinyl_svg"] = encoder.get_vinyl_overlay()
        base_data["vinyl_needle_svg"] = encoder.get_vinyl_needle()
    
    # apply theme-specific transformations
    theme_instance = ThemeRegistry.get_theme(config.theme, config.style, config.color)
    theme_data = theme_instance.transform_data(base_data)
    
    # ensure css variable is properly passed
    if "css" not in theme_data:
        theme_data["css"] = theme_instance.css
    
    # add request to context
    context = {"request": request, **theme_data}
    
    # select appropriate template based on theme
    template_name = "widget.html"  # default
    
    if config.theme == ThemeType.IPOD:
        template_name = "ipod.html"
    elif config.theme == ThemeType.VINYL:
        template_name = "vinyl.html"
        context["spin"] = True
        context["use_vinyl_svg"] = True
    elif config.theme == ThemeType.RETRO:
        template_name = "retro.html"
        context["show_equalizer"] = True
    elif config.theme == ThemeType.WINDOWS98:
        template_name = "windows98.html"
    
    # override with theme-specific template if provided
    if "template_name" in theme_data:
        template_name = theme_data["template_name"]
    
    # render the template to string
    content = templates.get_template(template_name).render(context)
    
    # fix any potential XML entity issues by properly encoding ampersands
    content = content.replace("&", "&amp;").replace("&amp;amp;", "&amp;")
    
    # return plain SVG response
    return Response(
        content=content,
        media_type="image/svg+xml"
    )


@app.get("/link", response_class=HTMLResponse)
async def get_link_page(
    request: Request,
    spotify_client: SpotifyApiClient = Depends(get_spotify_client)
):
    """generate page with embedded player"""
    track = await spotify_client.get_current_track()
    embed_link = f"https://open.spotify.com/embed/track/{track['id']}"
    
    return templates.TemplateResponse(
        "link.html", 
        {"request": request, "embed_link": embed_link}
    )