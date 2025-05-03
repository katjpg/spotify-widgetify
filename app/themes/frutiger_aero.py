from typing import Dict, Any
from app.themes.base import BaseTheme, ThemeCSS
from app.domain.models import ThemeStyle


class FrutigerAeroTheme(BaseTheme):
    """authentic windows vista/7 aero glass theme with glossy buttons and translucent effects"""
    
    @property
    def css(self) -> ThemeCSS:
        """get aero theme css variables using authentic vista/7 styling"""
        return ThemeCSS(
            background_color="#a7c7eb",        # gradient blue background base color
            title_color="#ffffff",             # white text with shadow for title
            subtitle_color="#ddddff",          # light blue-white for subtitle
            album_border_radius="3px",         # subtle rounded corners for album art
            container_padding="0px",           # no padding for the main container
            text_font="'Segoe UI', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', sans-serif"  # authentic Vista/7 font
        )
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """apply authentic frutiger aero glass transformations with glossy effects"""
        result = data.copy()
        
        # add theme-specific css variables
        result["css"] = self.css
        
        # add precise aero glass styling variables
        result["css"]["header_gradient"] = "linear-gradient(to bottom, #3a7ab3 0%, #346ea7 100%)"
        result["css"]["header_border"] = "#265786"
        result["css"]["header_shine"] = "linear-gradient(to bottom, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.1) 100%)"
        result["css"]["content_gradient"] = "linear-gradient(to bottom, #c4daf5 0%, #a7c7eb 100%)"
        result["css"]["glass_shine"] = "linear-gradient(to bottom, rgba(255, 255, 255, 0.7) 0%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0) 100%)"
        result["css"]["controls_gradient"] = "linear-gradient(to bottom, #cedce7 0%, #596a72 100%)"
        result["css"]["button_gradient"] = "linear-gradient(to bottom, #dce8f4 0%, #7c8d9e 100%)"
        result["css"]["button_shine"] = "linear-gradient(to bottom, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.1) 100%)"
        result["css"]["album_border"] = "rgba(255, 255, 255, 0.5)"
        result["css"]["album_shadow"] = "0 1px 4px rgba(0, 0, 0, 0.3)"
        result["css"]["text_shadow"] = "0 1px 2px rgba(0, 0, 0, 0.5)"
        
        # disable spinning and standard equalizer
        result["spin"] = False
        result["show_equalizer"] = False
        
        # add theme name for template logic
        result["theme_name"] = self.name
        
        # specify custom template
        result["template_name"] = "frutiger_aero.html"
        
        return result
    
    @property
    def supports_equalizer(self) -> bool:
        """aero theme doesn't use standard equalizer"""
        return False
        
    @property
    def supports_spin(self) -> bool:
        """aero theme doesn't use spinning album art"""
        return False