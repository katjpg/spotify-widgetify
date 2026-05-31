from typing import Any

from app.themes.base import BaseTheme, ThemeCSS

BACKGROUND = "#e2e2e3"
TITLE = "#555555"
SUBTITLE = "#666666"
CONTROLS_BG_DARK = "rgba(49,49,50,1)"
CONTROLS_BG_LIGHT = "rgba(255,255,255,1)"
CONTROLS_BORDER = "#e6e6e6"
CONTROLS_SHADOW = "0 4px 10px rgba(0, 0, 0, 0.05)"
ICON = "#b6b4b3"
ALBUM_BORDER = "#000000"


class IpodTheme(BaseTheme):
    """iPod click-wheel player with a circular control panel."""

    template = "ipod.html"

    @property
    def css(self) -> ThemeCSS:
        bg_color = self.color or BACKGROUND

        return ThemeCSS(
            background_color=bg_color,
            title_color=TITLE,
            subtitle_color=SUBTITLE,
            album_border_radius="20px",
            container_padding="15px",
            text_font="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif",
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        css = dict(self.css)

        css["controls_bg"] = self._dark_or_light(CONTROLS_BG_DARK, CONTROLS_BG_LIGHT)
        css["controls_border"] = CONTROLS_BORDER
        css["controls_shadow"] = CONTROLS_SHADOW
        css["icon_color"] = ICON
        css["album_border_color"] = ALBUM_BORDER
        css["album_border_width"] = "4px"
        # screen uses the album gradient; body keeps fixed chrome colors
        result["css"] = css
        return result
