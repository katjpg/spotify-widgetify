from functools import lru_cache
from typing import Type

from app.domain import ThemeName, ThemeStyle
from app.themes.base import BaseTheme
from app.themes.default import DefaultTheme
from app.themes.vinyl import VinylTheme
from app.themes.ipod import IpodTheme
from app.themes.retro import RetroTheme
from app.themes.windows98 import Windows98Theme
from app.themes.frutiger_aero import FrutigerAeroTheme
from app.themes.macintosh import MacintoshTheme
from app.themes.windowsxp import WindowsXPTheme


class ThemeRegistry:
    """Resolves a ThemeName to its theme, caching one instance per (theme, style, color)."""

    _themes: dict[ThemeName, Type[BaseTheme]] = {
        ThemeName.DEFAULT: DefaultTheme,
        ThemeName.VINYL: VinylTheme,
        ThemeName.IPOD: IpodTheme,
        ThemeName.RETRO: RetroTheme,
        ThemeName.WINDOWS98: Windows98Theme,
        ThemeName.FRUTIGER_AERO: FrutigerAeroTheme,
        ThemeName.MACINTOSH: MacintoshTheme,
        ThemeName.WINDOWSXP: WindowsXPTheme,
    }

    @classmethod
    @lru_cache(maxsize=20)
    def get_theme(
        cls, theme: ThemeName, style: ThemeStyle, color: str | None = None
    ) -> BaseTheme:
        theme_class = cls._themes.get(theme, DefaultTheme)
        return theme_class(style, color)

    @classmethod
    def register_theme(cls, theme: ThemeName, theme_class: Type[BaseTheme]) -> None:
        cls._themes[theme] = theme_class

    @classmethod
    def available_themes(cls) -> list[str]:
        return [t.value for t in cls._themes]
