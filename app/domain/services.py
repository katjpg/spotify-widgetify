from typing import Dict, Any

from app.domain.models import Track, WidgetConfig


class VisualizationService:
    """service for generating visual elements"""
    
    def __init__(self):
        """initialize with spectrum colors for equalizer"""
        self.spectrum = [
            "FF0000", "FF4000", "FF8000", "FFBF00", "FFFF00", 
            "BFFF00", "80FF00", "40FF00", "00FF00", "00FF40", 
            "00FF80", "00FFBF", "00FFFF", "00BFFF", "0080FF", 
            "0040FF", "0000FF", "4000FF", "8000FF", "BF00FF", "FF00FF"
        ]
    
    def generate_equalizer(self, bar_count: int, color: str) -> str:
        """generate html for equalizer visualization"""
        # skip generation if color is none
        if color.lower() == "none":
            return ""
            
        # for the new equalizer implementation, we don't need to generate HTML
        # we'll just use the template's built-in equalizer bars
        return ""

        
class ColorExtractionService:
    """service for extracting colors from images for dynamic backgrounds"""
    
    def __init__(self):
        """initialize with default colors"""
        self.default_colors = {
            "light": ["#F6F8FA", "#E1E4E8"],
            "dark": ["#161B22", "#0D1117"]
        }
    
    def extract_gradient_colors(self, album_image: str, is_dark: bool) -> Dict[str, str]:
        """
        extract gradient colors from album art for dynamic backgrounds
        since we can't process the image directly, we'll use predetermined colors
        based on the hash of the image
        """
        # fallback to default colors if image is empty
        if not album_image:
            colors = self.default_colors["dark" if is_dark else "light"]
            return {
                "primary_color": colors[0],
                "secondary_color": colors[1],
                "gradient": f"linear-gradient(135deg, {colors[0]}, {colors[1]})",
                "text_color": "#FFFFFF" if is_dark else "#000000"
            }
            
        # use a simple hash of the image to simulate color extraction
        image_hash = hash(album_image) % 1000
        
        # generate pseudo-random colors based on the hash
        hue = (image_hash % 360)
        saturation = 70 if is_dark else 40
        lightness_primary = 20 if is_dark else 80
        lightness_secondary = 30 if is_dark else 70
        
        primary = f"hsl({hue}, {saturation}%, {lightness_primary}%)"
        secondary = f"hsl({(hue + 30) % 360}, {saturation}%, {lightness_secondary}%)"
        
        return {
            "primary_color": primary,
            "secondary_color": secondary,
            "gradient": f"linear-gradient(135deg, {primary}, {secondary})",
            "text_color": "#FFFFFF" if is_dark else "#000000"
        }

class WidgetRenderingService:
    """service for preparing widget rendering data"""
    
    def __init__(self, visualization_service: VisualizationService, 
                color_extraction_service: ColorExtractionService = None):
        """initialize with required services"""
        self.visualization = visualization_service
        self.color_extraction = color_extraction_service or ColorExtractionService()
    
    def prepare_rendering_data(self, track: Track, config: WidgetConfig, 
                              spotify_logo: str) -> Dict[str, Any]:
        """prepare complete data for widget template rendering"""
        # determine bar count
        bar_count = 10  # fixed at 10 bars for the new equalizer
        
        # generate equalizer html if needed (now empty as we're using CSS directly)
        eq_bars_html = self.visualization.generate_equalizer(bar_count, config.eq_color)
        
        # extract colors for dynamic background if using vinyl theme
        dynamic_colors = {}
        if config.theme == "vinyl":
            is_dark = config.style == "dark"
            dynamic_colors = self.color_extraction.extract_gradient_colors(
                track["album_image"], is_dark
            )
        
        # return complete template data
        return {
            "track_name": track["name"],
            "track_artist": track["artist"],
            "track_id": track["id"],
            "base_64_track_image": track["album_image"],
            "logo": spotify_logo,
            "spin": config.spin,
            "eq_color": config.eq_color,
            "show_equalizer": config.eq_color.lower() != "none",
            "eq_bars_html": eq_bars_html,
            "config": config,
            "dynamic_colors": dynamic_colors
        }