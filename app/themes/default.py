from typing import Any

from app.services.color import ColorService
from app.themes.base import BaseTheme, ThemeCSS
from app.themes.palette import NowPlayingCard


class DefaultTheme(BaseTheme):
    """Album-gradient now-playing card, with an optional equalizer."""

    template = "widget.html"
    equalizer = True

    @property
    def css(self) -> ThemeCSS:
        bg_color = self.color or self._dark_or_light(
            NowPlayingCard.DARK_BG, NowPlayingCard.LIGHT_BG
        )

        return ThemeCSS(
            background_color=bg_color,
            title_color=NowPlayingCard.TITLE,
            subtitle_color=self._dark_or_light(
                NowPlayingCard.SUBTITLE_DARK, NowPlayingCard.SUBTITLE_LIGHT
            ),
            album_border_radius="10px",
            container_padding="20px",
            text_font="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif",
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        css = dict(self.css)
        # flat ?color= branch text; gradient branch uses palette.text
        css["base_text"] = ColorService.text_for(css["background_color"])
        result["css"] = css
        return result
