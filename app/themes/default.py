from typing import Dict, Any
from app.themes.base import BaseTheme, ThemeCSS
from app.domain.models import ThemeStyle


class DefaultTheme(BaseTheme):
    """default theme with equalizer visualization and blurred background"""
    
    @property
    def css(self) -> ThemeCSS:
        """get theme css variables"""
        # use custom color if provided, otherwise use default based on style
        bg_color = self.color if self.color else self._dark_or_light("#161B22", "#F6F8FA")
        
        return ThemeCSS(
            background_color=bg_color,
            title_color="#FFFFFF",  # always white text for visibility
            subtitle_color=self._dark_or_light("#BBBBBB", "#DDDDDD"),  # light gray for subtitle
            album_border_radius="10px",
            container_padding="20px",
            text_font="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
        )
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """apply default theme transformations"""
        result = data.copy()
        
        # add theme-specific css variables
        result["css"] = self.css
        
        # add overlay color for the blurred background effect
        if self.color:
            # override background and overlay with custom color
            # Use rgba format for overlay with 60% opacity
            color = self.color.lstrip('#')
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            result["css"]["overlay_color"] = f"rgba({r}, {g}, {b}, 0.6)"
        else:
            result["css"]["overlay_color"] = self._dark_or_light("rgba(0,0,0,0.6)", "rgba(0,0,0,0.25)")
        
        # update album radius if spinning
        if data.get("spin"):
            result["css"]["album_border_radius"] = "50%"
            
        # add theme name for template logic
        result["theme_name"] = self.name
        
        return result