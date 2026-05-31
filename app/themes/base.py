from abc import ABC, abstractmethod
from typing import Any, TypedDict

from app.domain import ThemeStyle


class ThemeCSS(TypedDict):
    background_color: str
    title_color: str
    subtitle_color: str
    album_border_radius: str
    container_padding: str
    text_font: str


class BaseTheme(ABC):
    """Presentation rules for one widget theme: its CSS, template, motion, and required assets."""

    template: str = "widget.html"
    required_assets: tuple[
        str, ...
    ] = ()  # asset keys the template needs, e.g. "vinyl_overlay"
    spins: bool = False
    equalizer: bool = False
    marquee_chars: int = 15  # titles longer than this overflow the marquee

    def __init__(self, style: ThemeStyle, color: str | None = None):
        self.style = style
        # accept a bare hex color and normalize to a css value
        self.color = f"#{color}" if color and not color.startswith("#") else color

    @property
    def is_dark(self) -> bool:
        return self.style is ThemeStyle.DARK

    @property
    @abstractmethod
    def css(self) -> ThemeCSS: ...

    @abstractmethod
    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]: ...

    def _dark_or_light(self, dark_value: str, light_value: str) -> str:
        return dark_value if self.is_dark else light_value
