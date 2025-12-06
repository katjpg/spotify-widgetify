from typing import Any

from app.themes.base import BaseTheme, ThemeCSS


class DefaultTheme(BaseTheme):
    """Default theme w/ equalizer and blurred background."""

    @property
    def css(self) -> ThemeCSS:
        bg_color = self.color or self._dark_or_light("#161B22", "#F6F8FA")

        return ThemeCSS(
            background_color=bg_color,
            title_color="#FFFFFF",
            subtitle_color=self._dark_or_light("#BBBBBB", "#DDDDDD"),
            album_border_radius="10px",
            container_padding="20px",
            text_font="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        result["css"] = self.css

        # overlay w/ custom color or default
        if self.color:
            color = self.color.lstrip('#')
            r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
            result["css"]["overlay_color"] = f"rgba({r}, {g}, {b}, 0.6)"
        else:
            result["css"]["overlay_color"] = self._dark_or_light("rgba(0,0,0,0.6)", "rgba(0,0,0,0.25)")

        if data.get("spin"):
            result["css"]["album_border_radius"] = "50%"

        result["theme_name"] = self.name
        return result
