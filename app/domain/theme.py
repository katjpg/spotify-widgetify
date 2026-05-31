from dataclasses import dataclass, replace
from enum import Enum


class ThemeStyle(str, Enum):
    LIGHT = "light"
    DARK = "dark"


class ThemeName(str, Enum):
    DEFAULT = "default"
    VINYL = "vinyl"
    IPOD = "ipod"
    RETRO = "retro"
    WINDOWS98 = "windows98"
    FRUTIGER_AERO = "frutiger_aero"
    MACINTOSH = "macintosh"
    WINDOWSXP = "windowsxp"


@dataclass(frozen=True, slots=True)
class Palette:
    primary: str  # gradient start stop, e.g. "rgb(34, 40, 49)"
    secondary: str  # gradient end stop
    text: str  # contrast token chosen by gradient luminance


# neutral palette for not-playing, missing art, or non-raster (SVG) artwork
FALLBACK_PALETTE = Palette(
    primary="rgb(34, 40, 49)", secondary="rgb(57, 62, 70)", text="#FFFFFF"
)


@dataclass(frozen=True, slots=True)
class WidgetConfig:
    theme: ThemeName = ThemeName.DEFAULT
    style: ThemeStyle = ThemeStyle.LIGHT
    color: str | None = None  # custom accent, hex digits without leading '#', or None
    eq_color: str = "1ED760"  # hex digits, "rainbow", or "none"

    @property
    def is_dark(self) -> bool:
        return self.style is ThemeStyle.DARK

    def with_color(self, color: str | None) -> "WidgetConfig":
        return replace(self, color=color)
