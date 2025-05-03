from typing import Dict, Any
from app.themes.base import BaseTheme, ThemeCSS
from app.domain.models import ThemeStyle


class RetroTheme(BaseTheme):
    """retro audio player-inspired theme with pixel-perfect design and static indicators"""
    
    @property
    def css(self) -> ThemeCSS:
        """get retro theme css variables with dotgothic16 font"""
        return ThemeCSS(
            background_color=self._dark_or_light("#232731", "#c6c6c6"),
            title_color=self._dark_or_light("#4df3ad", "#2eb532"),  # green text
            subtitle_color=self._dark_or_light("#3dd38d", "#269a2a"),  # lighter green text
            album_border_radius="4px",
            container_padding="15px",
            text_font="sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial"
        )
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """apply retro theme transformations with 8-bit styling and improved button design"""
        result = data.copy()
        
        # add theme-specific css variables
        result["css"] = self.css
        
        # border styling for 3D effect - different for dark and light modes
        result["css"]["border_top_color"] = self._dark_or_light("#181b22", "#9a9a9a")
        result["css"]["border_left_color"] = self._dark_or_light("#181b22", "#9a9a9a")
        result["css"]["border_right_color"] = self._dark_or_light("#40495f", "white")
        result["css"]["border_bottom_color"] = self._dark_or_light("#40495f", "white")
        result["css"]["button_border"] = self._dark_or_light("#12141c", "#9a9a9a")
        
        # retro-specific css variables for enhanced design
        result["css"]["panel_bg_color"] = self._dark_or_light("#10242f", "#041e2e")
        result["css"]["button_bg_color"] = self._dark_or_light("#303644", "#e1e1e1")
        result["css"]["button_color"] = self._dark_or_light("#4cf3ad", "#2fb532")
        result["css"]["equalizer_bar_color"] = self._dark_or_light("#4df3ad", "#0100fb")
        result["css"]["equalizer_progress_color"] = self._dark_or_light("#242424", "#181a29")
        result["css"]["overlay_color"] = self._dark_or_light("rgba(0,0,0,0.7)", "rgba(0,0,0,0.5)")
        
        # disable standard equalizer since we're using static dots
        result["show_equalizer"] = False
        
        # add theme name for template logic
        result["theme_name"] = self.name
        
        # use a custom template for retro theme
        result["template_name"] = "retro.html"
        
        return result
    
    @property
    def supports_equalizer(self) -> bool:
        """retro theme uses static indicators instead of dynamic equalizer"""
        return False
        
    @property
    def supports_spin(self) -> bool:
        """retro theme doesn't need spinning elements"""
        return False