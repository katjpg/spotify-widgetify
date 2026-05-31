from typing import Any

from app.themes.base import BaseTheme, ThemeCSS
from app.themes.palette import MacClassic


class MacintoshTheme(BaseTheme):
    """Classic 1984 Macintosh with monochrome Chicago type."""

    template = "macintosh.html"
    marquee_chars = 28  # wide marquee, small Chicago type

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color=MacClassic.WINDOW_GREY,
            title_color=MacClassic.INK,
            subtitle_color=MacClassic.PAPER,
            album_border_radius="0px",
            container_padding="0px",
            text_font="'Chicago', monospace",
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        result["css"] = dict(self.css)
        return result
