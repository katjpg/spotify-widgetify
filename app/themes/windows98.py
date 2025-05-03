from typing import Dict, Any
from app.themes.base import BaseTheme, ThemeCSS
from app.domain.models import ThemeStyle


class Windows98Theme(BaseTheme):
    """windows 98-inspired theme with classic cd player ui elements"""
    
    @property
    def css(self) -> ThemeCSS:
        """get windows 98 theme css variables"""
        return ThemeCSS(
            background_color="#C0C0C0",  # silver background
            title_color="#000000",       # black text
            subtitle_color="#000000",    # black text
            album_border_radius="0px",   # square corners for album art
            container_padding="1px",     # minimal padding
            text_font="'IBM Plex Mono', monospace"  # monospace font
        )
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """apply windows 98 theme transformations"""
        result = data.copy()
        
        # add theme-specific css variables
        result["css"] = self.css
        
        # add win98-specific styling variables
        result["css"]["titlebar_bg"] = "linear-gradient(to right, navy, rgb(16, 132, 208))"
        result["css"]["button_face"] = "#C0C0C0"
        result["css"]["button_highlight"] = "#FFFFFF"
        result["css"]["button_shadow"] = "#808080"
        result["css"]["button_dark_shadow"] = "#000000"
        
        # disable spinning and standard equalizer
        result["spin"] = False
        result["show_equalizer"] = False
        
        # add theme name for template logic
        result["theme_name"] = self.name
        
        # specify custom template
        result["template_name"] = "windows98.html"
        
        return result
    
    @property
    def supports_equalizer(self) -> bool:
        """windows 98 theme doesn't use standard equalizer"""
        return False
        
    @property
    def supports_spin(self) -> bool:
        """windows 98 theme doesn't use spinning album art"""
        return False