from typing import Any

from app.domain.models import Track, WidgetConfig


class WidgetRenderingService:
    """Prepares data for widget template rendering."""

    def prepare_rendering_data(
        self,
        track: Track,
        config: WidgetConfig,
        spotify_logo: str
    ) -> dict[str, Any]:
        """Build complete template context from track data and config."""
        return {
            "track_name": track.name,
            "track_artist": track.artist,
            "track_id": track.id,
            "base_64_track_image": track.album_image,
            "logo": spotify_logo,
            "spin": config.spin,
            "eq_color": config.eq_color,
            "show_equalizer": config.eq_color.lower() != "none",
            "config": config,
        }
