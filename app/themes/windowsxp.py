from typing import Any

from app.themes.base import BaseTheme, ThemeCSS


class WindowsXPTheme(BaseTheme):
    """Windows XP Media Player 11 theme."""

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color="#394152",
            title_color="#FFFFFF",
            subtitle_color="#CCCCCC",
            album_border_radius="0px",
            container_padding="0px",
            text_font="'Tahoma', sans-serif"
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        result["css"] = self.css

        result["spin"] = False
        result["show_equalizer"] = False
        result["theme_name"] = self.name
        result["template_name"] = "windowsxp.html"

        # wmp-specific vars
        result["css"]["player_active_white"] = "rgb(239, 247, 255)"
        result["css"]["player_disable_white"] = "rgba(239, 247, 255, 0.3)"
        result["css"]["gradient_top"] = "rgb(0, 0, 0)"
        result["css"]["gradient_middle"] = "rgb(57, 65, 82)"
        result["css"]["gradient_bottom_1"] = "rgb(102, 108, 132)"
        result["css"]["gradient_bottom_2"] = "rgb(17, 20, 25)"
        result["css"]["button_blue"] = "#00109c"
        result["css"]["control_shadow"] = "0 0 5px rgba(0, 82, 198, 0.5)"

        return result

    @property
    def supports_equalizer(self) -> bool:
        return False

    @property
    def supports_spin(self) -> bool:
        return False
