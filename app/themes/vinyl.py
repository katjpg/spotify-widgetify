from typing import Dict, Any
from app.themes.base import BaseTheme, ThemeCSS
from app.domain.models import ThemeStyle


class VinylTheme(BaseTheme):
    """vinyl record-inspired theme with blurred album art background"""
    
    @property
    def css(self) -> ThemeCSS:
        """get vinyl theme css variables"""
        # use custom color if provided, otherwise use default based on style
        bg_color = self.color if self.color else self._dark_or_light("#161B22", "#F6F8FA")
        
        base_css = ThemeCSS(
            background_color=bg_color,
            title_color="#FFFFFF",  # always white text for visibility
            subtitle_color=self._dark_or_light("#BBBBBB", "#DDDDDD"), 
            album_border_radius="50%",  # always circular
            container_padding="20px",
            text_font="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif"
        )
        
        # create overlay color with transparency from custom color or default
        overlay_color = "rgba(0,0,0,0.6)"
        if self.color:
            # Strip # if present and convert to rgba
            color = self.color.lstrip('#')
            if len(color) == 6:
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4:6], 16)
                overlay_color = f"rgba({r}, {g}, {b}, 0.6)"
        else:
            overlay_color = self._dark_or_light("rgba(0,0,0,0.6)", "rgba(0,0,0,0.45)")
        
        # vinyl-specific css variables
        vinyl_css = {
            "overlay_color": overlay_color,
            "spin_duration": "10s",  # consistent spin duration for vinyl and album
            "container_padding": "15px",  # reduced padding to fit in smaller container
        }
        
        # add vinyl-specific css vars to base css
        result = dict(base_css)
        result.update(vinyl_css)
        
        return result
    
    def transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """apply vinyl theme transformations"""
        result = data.copy()
        
        # vinyl theme forces spin and disables equalizer
        result["spin"] = True
        result["show_equalizer"] = False
        
        # add vinyl-specific template data
        result["css"] = self.css
        result["theme_name"] = self.name
        result["use_vinyl_svg"] = True
        
        # explicitly set template name to be used in main.py
        result["template_name"] = "vinyl.html"
        
        return result
    
    @property
    def supports_equalizer(self) -> bool:
        """vinyl theme doesn't use equalizer"""
        return False