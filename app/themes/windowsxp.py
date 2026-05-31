from typing import Any

from app.themes.base import BaseTheme, ThemeCSS
from app.themes.palette import Wmp11


class WindowsXPTheme(BaseTheme):
    """Windows XP Media Player 11 with a glossy blue console."""

    template = "windowsxp.html"

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color=Wmp11.BACKGROUND,
            title_color=Wmp11.TITLE,
            subtitle_color=Wmp11.SUBTITLE,
            album_border_radius="0px",
            container_padding="0px",
            text_font="'Tahoma', sans-serif",
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        css = dict(self.css)

        css["player_active_white"] = Wmp11.ACTIVE_WHITE
        css["player_disable_white"] = Wmp11.DISABLE_WHITE
        css["gradient_top"] = Wmp11.GRADIENT_TOP
        css["gradient_middle"] = Wmp11.GRADIENT_MIDDLE
        css["gradient_bottom_1"] = Wmp11.GRADIENT_BOTTOM_1
        css["gradient_bottom_2"] = Wmp11.GRADIENT_BOTTOM_2
        css["button_blue"] = Wmp11.BUTTON_BLUE
        css["control_shadow"] = Wmp11.CONTROL_SHADOW

        result["css"] = css
        return result
