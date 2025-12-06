from typing import Any

from app.domain.models import Track, WidgetConfig

# char limits for marquee trigger (based on container width & font size)
MARQUEE_CHAR_LIMITS: dict[str, int] = {
    "default": 18,
    "ipod": 16,
    "vinyl": 20,
    "retro": 18,
    "windows98": 22,
    "windowsxp": 20,
    "frutiger_aero": 20,
    "macintosh": 18,
}


class WidgetRenderingService:
    """Prepares data for widget template rendering."""

    def prepare_rendering_data(
        self,
        track: Track,
        config: WidgetConfig,
        spotify_logo: str
    ) -> dict[str, Any]:
        """Build complete template context from track data and config."""
        char_limit = MARQUEE_CHAR_LIMITS.get(config.theme.value, 18)

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
            "marquee_track_name": len(track.name) > char_limit,
            "marquee_track_artist": len(track.artist) > char_limit,
        }
