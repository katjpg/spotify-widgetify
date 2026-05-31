from dataclasses import dataclass
from typing import Any

from app.assets.images import ImageEncoder
from app.domain import Track, WidgetConfig
from app.themes.registry import ThemeRegistry


@dataclass(frozen=True, slots=True)
class RenderContext:
    template_name: str
    context: dict[str, Any]  # Jinja variables, excluding "request"


class RenderingService:
    """Builds the template and Jinja context for a Track under a WidgetConfig."""

    def __init__(self, encoder: ImageEncoder):
        self._encoder = encoder

    def render_widget(self, track: Track, config: WidgetConfig) -> RenderContext:
        theme = ThemeRegistry.get_theme(config.theme, config.style, config.color)

        context: dict[str, Any] = {
            "track_name": track.title,
            "track_artist": track.artist,
            "track_id": track.track_id,
            "base_64_track_image": track.album_art,
            "logo": self._encoder.get_spotify_logo(),
            "spin": theme.spins,
            "show_equalizer": theme.equalizer and config.eq_color.lower() != "none",
            "palette": track.palette,
            "has_color": config.color is not None,
            # longer titles get proportionally longer durations for a constant scroll speed
            "marquee_duration": f"{max(12, round(len(track.title) * 0.4))}s",
        }
        if "vinyl_overlay" in theme.required_assets:
            context["vinyl_svg"] = self._encoder.get_vinyl_overlay()
        if "vinyl_needle" in theme.required_assets:
            context["vinyl_needle_svg"] = self._encoder.get_vinyl_needle()

        context = theme.transform_data(context)
        return RenderContext(template_name=theme.template, context=context)
