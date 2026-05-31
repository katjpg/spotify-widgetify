from typing import Any

from app.services.color import ColorService
from app.themes.base import BaseTheme, ThemeCSS
from app.themes.palette import NowPlayingCard

SCRIM_LIGHT = "rgba(0,0,0,0.45)"
SCRIM_DARK = "rgba(0,0,0,0.6)"


class VinylTheme(BaseTheme):
    """Spinning vinyl record with the album art at its center."""

    template = "vinyl.html"
    required_assets = ("vinyl_overlay", "vinyl_needle")
    spins = True

    @property
    def css(self) -> ThemeCSS:
        bg_color = self.color or self._dark_or_light(
            NowPlayingCard.DARK_BG, NowPlayingCard.LIGHT_BG
        )

        base_css = ThemeCSS(
            background_color=bg_color,
            title_color=NowPlayingCard.TITLE,
            subtitle_color=self._dark_or_light(
                NowPlayingCard.SUBTITLE_DARK, NowPlayingCard.SUBTITLE_LIGHT
            ),
            album_border_radius="50%",
            container_padding="15px",
            text_font="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif",
        )

        result = dict(base_css)
        result["overlay_color"] = ColorService.palette(
            self.color,
            self.is_dark,
            light_default=SCRIM_LIGHT,
            dark_default=SCRIM_DARK,
            guard_six=True,
        ).overlay
        result["spin_duration"] = "10s"
        return result

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        result["css"] = self.css
        return result
