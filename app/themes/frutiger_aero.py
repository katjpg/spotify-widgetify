from typing import Any

from app.themes.base import BaseTheme, ThemeCSS


class FrutigerAeroTheme(BaseTheme):
    """Windows Vista/7 Aero glass theme."""

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color="#a7c7eb",
            title_color="#ffffff",
            subtitle_color="#ddddff",
            album_border_radius="3px",
            container_padding="0px",
            text_font="'Segoe UI', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', sans-serif"
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        result["css"] = self.css

        # aero glass vars
        result["css"]["header_gradient"] = "linear-gradient(to bottom, #3a7ab3 0%, #346ea7 100%)"
        result["css"]["header_border"] = "#265786"
        result["css"]["header_shine"] = "linear-gradient(to bottom, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.1) 100%)"
        result["css"]["content_gradient"] = "linear-gradient(to bottom, #c4daf5 0%, #a7c7eb 100%)"
        result["css"]["glass_shine"] = "linear-gradient(to bottom, rgba(255, 255, 255, 0.7) 0%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0) 100%)"
        result["css"]["controls_gradient"] = "linear-gradient(to bottom, #cedce7 0%, #596a72 100%)"
        result["css"]["button_gradient"] = "linear-gradient(to bottom, #dce8f4 0%, #7c8d9e 100%)"
        result["css"]["button_shine"] = "linear-gradient(to bottom, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.1) 100%)"
        result["css"]["album_border"] = "rgba(255, 255, 255, 0.5)"
        result["css"]["album_shadow"] = "0 1px 4px rgba(0, 0, 0, 0.3)"
        result["css"]["text_shadow"] = "0 1px 2px rgba(0, 0, 0, 0.5)"

        result["spin"] = False
        result["show_equalizer"] = False
        result["theme_name"] = self.name
        result["template_name"] = "frutiger_aero.html"

        return result

    @property
    def supports_equalizer(self) -> bool:
        return False

    @property
    def supports_spin(self) -> bool:
        return False
