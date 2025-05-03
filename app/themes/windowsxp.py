from typing import Dict, Any
from app.themes.base import BaseTheme, ThemeCSS
from app.domain.models import ThemeStyle


class WindowsXPTheme(BaseTheme):
    """windows xp media player 11 inspired theme with classic wmp interface"""
    
    @property
    def css(self) -> ThemeCSS:
        """get windows xp theme css variables"""
        return ThemeCSS(
            background_color="#394152",  # base gradient color for the player
            title_color="#FFFFFF",       # white text for the title
            subtitle_color="#CCCCCC",    # light gray for artist name
            album_border_radius="0px",   # square corners for album art (authentic to WMP)
            container_padding="0px",     # no padding for the main container
            text_font="'Tahoma', sans-serif"  # tahoma font as requested
        )
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """apply windows xp media player theme transformations"""
        result = data.copy()
        
        # add theme-specific css variables
        result["css"] = self.css
        
        # windows xp theme doesn't use standard equalizer or spinning
        result["spin"] = False
        result["show_equalizer"] = False
        
        # add theme name for template logic
        result["theme_name"] = self.name
        
        # specify custom template
        result["template_name"] = "windowsxp.html"
        
        # add wmp-specific styling variables
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
        """windows xp theme uses its own visualization rather than standard equalizer"""
        return False
        
    @property
    def supports_spin(self) -> bool:
        """windows xp theme doesn't use spinning album art"""
        return False