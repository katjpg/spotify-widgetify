from typing import Any

from app.themes.base import BaseTheme, ThemeCSS


class Windows98Theme(BaseTheme):
    """Windows 98 CD player theme."""

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color="#C0C0C0",
            title_color="#000000",
            subtitle_color="#000000",
            album_border_radius="0px",
            container_padding="1px",
            text_font="'IBM Plex Mono', monospace"
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        result["css"] = self.css

        # win98-specific vars
        result["css"]["titlebar_bg"] = "linear-gradient(to right, navy, rgb(16, 132, 208))"
        result["css"]["button_face"] = "#C0C0C0"
        result["css"]["button_highlight"] = "#FFFFFF"
        result["css"]["button_shadow"] = "#808080"
        result["css"]["button_dark_shadow"] = "#000000"

        result["spin"] = False
        result["show_equalizer"] = False
        result["theme_name"] = self.name
        result["template_name"] = "windows98.html"

        return result

    @property
    def supports_equalizer(self) -> bool:
        return False

    @property
    def supports_spin(self) -> bool:
        return False
