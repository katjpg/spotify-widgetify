from typing import Any

from app.themes.base import BaseTheme, ThemeCSS


class VinylTheme(BaseTheme):
    """Vinyl record theme w/ spinning album art."""

    @property
    def css(self) -> ThemeCSS:
        bg_color = self.color or self._dark_or_light("#161B22", "#F6F8FA")

        base_css = ThemeCSS(
            background_color=bg_color,
            title_color="#FFFFFF",
            subtitle_color=self._dark_or_light("#BBBBBB", "#DDDDDD"),
            album_border_radius="50%",
            container_padding="15px",
            text_font="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
        )

        # overlay from custom color or default
        if self.color:
            color = self.color.lstrip('#')
            if len(color) == 6:
                r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
                overlay_color = f"rgba({r}, {g}, {b}, 0.6)"
            else:
                overlay_color = "rgba(0,0,0,0.6)"
        else:
            overlay_color = self._dark_or_light("rgba(0,0,0,0.6)", "rgba(0,0,0,0.45)")

        result = dict(base_css)
        result["overlay_color"] = overlay_color
        result["spin_duration"] = "10s"

        return result

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()

        result["spin"] = True
        result["show_equalizer"] = False
        result["css"] = self.css
        result["theme_name"] = self.name
        result["use_vinyl_svg"] = True
        result["template_name"] = "vinyl.html"

        return result

    @property
    def supports_equalizer(self) -> bool:
        return False
