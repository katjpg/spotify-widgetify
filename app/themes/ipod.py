from typing import Any

from app.themes.base import BaseTheme, ThemeCSS


class IpodTheme(BaseTheme):
    """iPod-inspired theme w/ circular control panel."""

    @property
    def css(self) -> ThemeCSS:
        bg_color = self.color or "#e2e2e3"

        return ThemeCSS(
            background_color=bg_color,
            title_color="#555555",
            subtitle_color="#666666",
            album_border_radius="20px",
            container_padding="15px",
            text_font="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()

        result["css"] = self.css
        result["spin"] = False
        result["show_equalizer"] = False
        result["theme_name"] = self.name

        # ipod-specific vars
        result["css"]["controls_bg"] = self._dark_or_light("rgba(49,49,50,1)", "rgba(255,255,255,1)")
        result["css"]["controls_border"] = "#e6e6e6"
        result["css"]["controls_shadow"] = "0 4px 10px rgba(0, 0, 0, 0.05)"
        result["css"]["icon_color"] = "#b6b4b3"
        result["css"]["album_border_color"] = "#000000"
        result["css"]["album_border_width"] = "4px"
        result["css"]["overlay_color"] = self._dark_or_light("rgba(0,0,0,0.6)", "rgba(0,0,0,0.45)")

        return result

    @property
    def supports_equalizer(self) -> bool:
        return False

    @property
    def supports_spin(self) -> bool:
        return False
