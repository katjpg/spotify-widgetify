from abc import ABC, abstractmethod
from typing import Any, TypedDict

from app.domain.models import ThemeStyle


class ThemeCSS(TypedDict):
    background_color: str
    title_color: str
    subtitle_color: str
    album_border_radius: str
    container_padding: str
    text_font: str


class BaseTheme(ABC):
    """Abstract base for widget themes."""

    def __init__(self, style: ThemeStyle, color: str | None = None):
        self.style = style
        self.color = f"#{color}" if color and not color.startswith('#') else color

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower().replace('theme', '')

    @property
    def is_dark(self) -> bool:
        return self.style == ThemeStyle.DARK

    @property
    @abstractmethod
    def css(self) -> ThemeCSS:
        pass

    @abstractmethod
    def transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    @property
    def supports_equalizer(self) -> bool:
        return True

    @property
    def supports_spin(self) -> bool:
        return True

    def _dark_or_light(self, dark_value: str, light_value: str) -> str:
        return dark_value if self.is_dark else light_value
