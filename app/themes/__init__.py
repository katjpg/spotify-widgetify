from typing import Dict, Type, Optional
from functools import lru_cache
from app.themes.base import BaseTheme
from app.themes.default import DefaultTheme
from app.themes.vinyl import VinylTheme
from app.themes.ipod import IpodTheme
from app.themes.retro import RetroTheme
from app.themes.windows98 import Windows98Theme
from app.themes.frutiger_aero import FrutigerAeroTheme
from app.themes.macintosh import MacintoshTheme
from app.themes.windowsxp import WindowsXPTheme  # Import the new theme
from app.domain.models import ThemeType, ThemeStyle


class ThemeRegistry:
    """registry and factory for widget themes"""
    
    # theme class registry
    _themes: Dict[ThemeType, Type[BaseTheme]] = {
        ThemeType.DEFAULT: DefaultTheme,
        ThemeType.VINYL: VinylTheme,
        ThemeType.IPOD: IpodTheme,
        ThemeType.RETRO: RetroTheme,
        ThemeType.WINDOWS98: Windows98Theme,
        ThemeType.FRUTIGER_AERO: FrutigerAeroTheme,
        ThemeType.MACINTOSH: MacintoshTheme,
        ThemeType.WINDOWSXP: WindowsXPTheme,  # Register the new theme
    }
    
    @classmethod
    @lru_cache(maxsize=20)  # increased for color variations
    def get_theme(cls, theme: ThemeType, style: ThemeStyle, color: Optional[str] = None) -> BaseTheme:
        """get appropriate theme instance with caching"""
        theme_class = cls._themes.get(theme, DefaultTheme)
        return theme_class(style, color)
    
    @classmethod
    def register_theme(cls, theme_type: ThemeType, theme_class: Type[BaseTheme]) -> None:
        """register a new theme type"""
        cls._themes[theme_type] = theme_class
    
    @classmethod
    def available_themes(cls) -> list[str]:
        """get list of available theme names"""
        return [t.value for t in cls._themes.keys()]