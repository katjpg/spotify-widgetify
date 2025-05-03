from abc import ABC, abstractmethod
from typing import Dict, Any, TypedDict, Optional
from app.domain.models import ThemeStyle


class ThemeCSS(TypedDict):
    """strongly typed theme css variables"""
    background_color: str
    title_color: str
    subtitle_color: str
    album_border_radius: str
    container_padding: str
    text_font: str


class BaseTheme(ABC):
    """abstract base theme interface"""
    
    def __init__(self, style: ThemeStyle, color: Optional[str] = None):
        """initialize with theme style and optional color"""
        self.style = style
        # ensure color has proper hex format with leading #
        self.color = f"#{color}" if color and not color.startswith('#') else color
    
    @property
    def name(self) -> str:
        """get theme name from class name"""
        return self.__class__.__name__.lower().replace('theme', '')
    
    @property
    def is_dark(self) -> bool:
        """check if theme is in dark mode"""
        return self.style == ThemeStyle.DARK
    
    @property
    @abstractmethod
    def css(self) -> ThemeCSS:
        """get theme css variables"""
        pass
    
    @abstractmethod
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """apply theme-specific transformations to template data"""
        pass
    
    @property
    def supports_equalizer(self) -> bool:
        """whether theme supports equalizer visualization"""
        return True
    
    @property
    def supports_spin(self) -> bool:
        """whether theme supports album art spinning"""
        return True
    
    def _dark_or_light(self, dark_value: str, light_value: str) -> str:
        """helper to get style-appropriate value"""
        return dark_value if self.is_dark else light_value