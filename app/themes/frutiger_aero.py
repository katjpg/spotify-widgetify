from typing import Any

from app.themes.base import BaseTheme, ThemeCSS
from app.themes.palette import AeroGlass


class FrutigerAeroTheme(BaseTheme):
    """Windows Vista/7 Aero glass with layered shine gradients."""

    template = "frutiger_aero.html"
    marquee_chars = 24  # wide 260px marquee

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color=AeroGlass.BACKGROUND,
            title_color=AeroGlass.TITLE,
            subtitle_color=AeroGlass.SUBTITLE,
            album_border_radius="3px",
            container_padding="0px",
            text_font="'Segoe UI', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', sans-serif",
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        css = dict(self.css)

        css["header_gradient"] = AeroGlass.HEADER_GRADIENT
        css["header_border"] = AeroGlass.HEADER_BORDER
        css["header_shine"] = AeroGlass.HEADER_SHINE
        css["content_gradient"] = AeroGlass.CONTENT_GRADIENT
        css["glass_shine"] = AeroGlass.GLASS_SHINE
        css["controls_gradient"] = AeroGlass.CONTROLS_GRADIENT
        css["button_gradient"] = AeroGlass.BUTTON_GRADIENT
        css["button_shine"] = AeroGlass.BUTTON_SHINE
        css["album_border"] = AeroGlass.ALBUM_BORDER
        css["album_shadow"] = AeroGlass.ALBUM_SHADOW
        css["text_shadow"] = AeroGlass.TEXT_SHADOW

        result["css"] = css
        return result
