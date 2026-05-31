from typing import Any

from app.themes.base import BaseTheme, ThemeCSS

BG_DARK = "#232731"
BG_LIGHT = "#c6c6c6"
TITLE_DARK = "#4df3ad"
TITLE_LIGHT = "#2eb532"
SUBTITLE_DARK = "#3dd38d"
SUBTITLE_LIGHT = "#269a2a"
BEVEL_TL_DARK = "#181b22"
BEVEL_TL_LIGHT = "#9a9a9a"
BEVEL_BR_DARK = "#40495f"
BEVEL_BR_LIGHT = "white"
BUTTON_BORDER_DARK = "#12141c"
BUTTON_BORDER_LIGHT = "#9a9a9a"
PANEL_DARK = "#10242f"
PANEL_LIGHT = "#041e2e"
BUTTON_BG_DARK = "#303644"
BUTTON_BG_LIGHT = "#e1e1e1"
BUTTON_DARK = "#4cf3ad"
BUTTON_LIGHT = "#2fb532"
EQ_BAR_DARK = "#4df3ad"
EQ_BAR_LIGHT = "#0100fb"
EQ_PROGRESS_DARK = "#242424"
EQ_PROGRESS_LIGHT = "#181a29"
SCRIM_DARK = "rgba(0,0,0,0.7)"
SCRIM_LIGHT = "rgba(0,0,0,0.5)"


class RetroTheme(BaseTheme):
    """CRT-era audio player with a 3D-bevelled panel and equalizer."""

    template = "retro.html"

    @property
    def css(self) -> ThemeCSS:
        return ThemeCSS(
            background_color=self._dark_or_light(BG_DARK, BG_LIGHT),
            title_color=self._dark_or_light(TITLE_DARK, TITLE_LIGHT),
            subtitle_color=self._dark_or_light(SUBTITLE_DARK, SUBTITLE_LIGHT),
            album_border_radius="4px",
            container_padding="15px",
            text_font="sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial",
        )

    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        result = data.copy()
        css = dict(self.css)

        # 3D border bevel
        css["border_top_color"] = self._dark_or_light(BEVEL_TL_DARK, BEVEL_TL_LIGHT)
        css["border_left_color"] = self._dark_or_light(BEVEL_TL_DARK, BEVEL_TL_LIGHT)
        css["border_right_color"] = self._dark_or_light(BEVEL_BR_DARK, BEVEL_BR_LIGHT)
        css["border_bottom_color"] = self._dark_or_light(BEVEL_BR_DARK, BEVEL_BR_LIGHT)
        css["button_border"] = self._dark_or_light(
            BUTTON_BORDER_DARK, BUTTON_BORDER_LIGHT
        )

        css["panel_bg_color"] = self._dark_or_light(PANEL_DARK, PANEL_LIGHT)
        css["button_bg_color"] = self._dark_or_light(BUTTON_BG_DARK, BUTTON_BG_LIGHT)
        css["button_color"] = self._dark_or_light(BUTTON_DARK, BUTTON_LIGHT)
        css["equalizer_bar_color"] = self._dark_or_light(EQ_BAR_DARK, EQ_BAR_LIGHT)
        css["equalizer_progress_color"] = self._dark_or_light(
            EQ_PROGRESS_DARK, EQ_PROGRESS_LIGHT
        )
        css["overlay_color"] = self._dark_or_light(SCRIM_DARK, SCRIM_LIGHT)

        result["css"] = css
        return result
