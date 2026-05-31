from typing import Any

from app.themes.base import BaseTheme, ThemeCSS
from app.themes.palette import Win9xBevel

WINDOW_TEXT = "#000000"
TITLEBAR_BG = "linear-gradient(to right, navy, rgb(16, 132, 208))"


class Windows98Theme(BaseTheme):
    """Windows 98 CD player with raised-bevel chrome."""

    template = "windows98.html"

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color=Win9xBevel.FACE,
            title_color=WINDOW_TEXT,
            subtitle_color=WINDOW_TEXT,
            album_border_radius="0px",
            container_padding="1px",
            text_font="'IBM Plex Mono', monospace",
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        css = dict(self.css)

        css["titlebar_bg"] = TITLEBAR_BG
        css["button_face"] = Win9xBevel.FACE
        css["button_highlight"] = Win9xBevel.HIGHLIGHT
        css["button_shadow"] = Win9xBevel.SHADOW
        css["button_dark_shadow"] = Win9xBevel.DARK_SHADOW

        result["css"] = css
        return result
