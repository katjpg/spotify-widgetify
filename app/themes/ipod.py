from typing import Dict, Any
from app.themes.base import BaseTheme, ThemeCSS
from app.domain.models import ThemeStyle


class IpodTheme(BaseTheme):
    """ipod-inspired theme with circular control panel design"""
    
    @property
    def css(self) -> ThemeCSS:
        """get ipod theme css variables"""
        # use custom color if provided, otherwise use default
        bg_color = self.color if self.color else "#e2e2e3"
        
        return ThemeCSS(
            background_color=bg_color,  # custom color affects the ipod body
            title_color="#555555",
            subtitle_color="#666666",
            album_border_radius="20px",
            container_padding="15px",
            text_font="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
        )
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """apply ipod theme transformations"""
        result = data.copy()
        
        # add theme-specific css variables
        result["css"] = self.css
        
        # ipod theme doesn't use equalizer or spinning
        result["spin"] = False
        result["show_equalizer"] = False
        
        # add theme name for template logic
        result["theme_name"] = self.name
        
        # add ipod-specific styling variables
        result["css"]["controls_bg"] = self._dark_or_light("rgba(49,49,50,1)", "rgba(255,255,255,1)")
        result["css"]["controls_border"] = "#e6e6e6"
        result["css"]["controls_shadow"] = "0 4px 10px rgba(0, 0, 0, 0.05)"
        result["css"]["icon_color"] = "#b6b4b3"
        result["css"]["album_border_color"] = "#000000"
        result["css"]["album_border_width"] = "4px"
        result["css"]["overlay_color"] = self._dark_or_light("rgba(0,0,0,0.6)", "rgba(0,0,0,0.45)")
        
        # For debugging - log what color is being used
        print(f"IpodTheme using background color: {result['css']['background_color']}")
        
        return result
    
    @property
    def supports_equalizer(self) -> bool:
        """ipod theme doesn't use equalizer visualization"""
        return False
        
    @property
    def supports_spin(self) -> bool:
        """ipod theme doesn't support album art spinning"""
        return False