from typing import Any

from app.themes.base import BaseTheme, ThemeCSS


class MacintoshTheme(BaseTheme):
    """Classic 1983 Macintosh theme."""

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color="#E8E8E8",
            title_color="#000000",
            subtitle_color="#FFFFFF",
            album_border_radius="0px",
            container_padding="0px",
            text_font="'Chicago', monospace"
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        result["css"] = self.css

        result["spin"] = False
        result["show_equalizer"] = False
        result["theme_name"] = self.name
        result["template_name"] = "macintosh.html"

        return result

    @property
    def supports_equalizer(self) -> bool:
        return False

    @property
    def supports_spin(self) -> bool:
        return False
