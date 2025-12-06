from typing import Any

from app.themes.base import BaseTheme, ThemeCSS


class RetroTheme(BaseTheme):
    """Retro audio player theme w/ pixel-perfect design."""

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color=self._dark_or_light("#232731", "#c6c6c6"),
            title_color=self._dark_or_light("#4df3ad", "#2eb532"),
            subtitle_color=self._dark_or_light("#3dd38d", "#269a2a"),
            album_border_radius="4px",
            container_padding="15px",
            text_font="sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial"
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        result["css"] = self.css

        # 3D border effect
        result["css"]["border_top_color"] = self._dark_or_light("#181b22", "#9a9a9a")
        result["css"]["border_left_color"] = self._dark_or_light("#181b22", "#9a9a9a")
        result["css"]["border_right_color"] = self._dark_or_light("#40495f", "white")
        result["css"]["border_bottom_color"] = self._dark_or_light("#40495f", "white")
        result["css"]["button_border"] = self._dark_or_light("#12141c", "#9a9a9a")

        # retro-specific vars
        result["css"]["panel_bg_color"] = self._dark_or_light("#10242f", "#041e2e")
        result["css"]["button_bg_color"] = self._dark_or_light("#303644", "#e1e1e1")
        result["css"]["button_color"] = self._dark_or_light("#4cf3ad", "#2fb532")
        result["css"]["equalizer_bar_color"] = self._dark_or_light("#4df3ad", "#0100fb")
        result["css"]["equalizer_progress_color"] = self._dark_or_light("#242424", "#181a29")
        result["css"]["overlay_color"] = self._dark_or_light("rgba(0,0,0,0.7)", "rgba(0,0,0,0.5)")

        result["show_equalizer"] = False
        result["theme_name"] = self.name
        result["template_name"] = "retro.html"

        return result

    @property
    def supports_equalizer(self) -> bool:
        return False

    @property
    def supports_spin(self) -> bool:
        return False
