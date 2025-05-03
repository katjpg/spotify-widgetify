from typing import Dict, Any
from app.themes.base import BaseTheme, ThemeCSS
from app.domain.models import ThemeStyle


class MacintoshTheme(BaseTheme):
    """macintosh-inspired theme with classic apple UI design from 1983"""
    
    @property
    def css(self) -> ThemeCSS:
        """get macintosh theme css variables"""
        return ThemeCSS(
            background_color="#E8E8E8",  # Light gray background
            title_color="#000000",       # Black text
            subtitle_color="#FFFFFF",    # White subtitle (for display on black background)
            album_border_radius="0px",   # Square corners for album art (authentic to old Mac)
            container_padding="0px",     # No padding for the main container
            text_font="'Chicago', monospace"  # Chicago font (the iconic Mac font)
        )
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """apply macintosh theme transformations"""
        result = data.copy()
        
        # add theme-specific css variables
        result["css"] = self.css
        
        # macintosh theme doesn't use equalizer or spinning
        result["spin"] = False
        result["show_equalizer"] = False
        
        # add theme name for template logic
        result["theme_name"] = self.name
        
        # specify custom template
        result["template_name"] = "macintosh.html"
        
        return result
    
    @property
    def supports_equalizer(self) -> bool:
        """macintosh theme doesn't use standard equalizer"""
        return False
        
    @property
    def supports_spin(self) -> bool:
        """macintosh theme doesn't support album art spinning"""
        return False