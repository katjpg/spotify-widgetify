from typing import TypedDict, Optional
from enum import Enum
from dataclasses import dataclass


class ThemeStyle(str, Enum):
    """theme light/dark mode style"""
    LIGHT = "light"
    DARK = "dark"


class ThemeType(str, Enum):
    """available theme types"""
    DEFAULT = "default"
    VINYL = "vinyl"
    IPOD = "ipod"
    RETRO = "retro"
    WINDOWS98 = "windows98"
    FRUTIGER_AERO = "frutiger_aero"
    MACINTOSH = "macintosh"
    WINDOWSXP = "windowsxp"


class Track(TypedDict):
    """track data structure"""
    name: str
    artist: str
    album_image: str
    uri: str
    id: str


@dataclass
class WidgetConfig:
    """configuration for widget rendering"""
    theme: ThemeType
    style: ThemeStyle
    color: Optional[str] = None
    spin: bool = False
    eq_color: str = "1ED760"
    
    @classmethod
    def from_query_params(cls, 
                         theme: str = "default", 
                         style: str = "light", 
                         color: Optional[str] = None,
                         spin: bool = False, 
                         eq_color: str = "1ED760") -> "WidgetConfig":
        """create config from query parameters"""
        theme_type = ThemeType(theme)
        
        # windows98 theme only has light style
        theme_style = ThemeStyle.LIGHT if theme_type == ThemeType.WINDOWS98 else ThemeStyle(style)
        
        # color only available for specific themes
        valid_color = None
        if color and theme_type in [ThemeType.IPOD, ThemeType.VINYL, ThemeType.DEFAULT]:
            # Ensure color is a valid hex code (strip leading # if present)
            valid_color = color.lstrip('#')
            print(f"Processing color parameter: {color} -> {valid_color}")
        
        return cls(
            theme=theme_type,
            style=theme_style,
            color=valid_color,
            spin=spin,
            eq_color=eq_color
        )