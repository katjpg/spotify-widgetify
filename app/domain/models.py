from typing import Annotated
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from pydantic.functional_validators import AfterValidator


class ThemeStyle(str, Enum):
    LIGHT = "light"
    DARK = "dark"


class ThemeType(str, Enum):
    DEFAULT = "default"
    VINYL = "vinyl"
    IPOD = "ipod"
    RETRO = "retro"
    WINDOWS98 = "windows98"
    FRUTIGER_AERO = "frutiger_aero"
    MACINTOSH = "macintosh"
    WINDOWSXP = "windowsxp"


def _validate_eq_color(v: str) -> str:
    """Validate equalizer color - accepts hex, 'rainbow', or 'none'."""
    if v.lower() in ('rainbow', 'none'):
        return v.lower()
    v = v.lstrip('#')
    if len(v) not in (3, 6) or not all(c in '0123456789ABCDEFabcdef' for c in v):
        raise ValueError('Invalid hex color')
    return v


EqColor = Annotated[str, AfterValidator(_validate_eq_color)]


class Track(BaseModel):
    name: str = Field(default="Not Playing")
    artist: str = Field(default="")
    album_image: str = Field(default="")
    uri: str = Field(default="")
    id: str = Field(default="")


# themes that support custom colors
COLOR_SUPPORTED_THEMES = {ThemeType.IPOD, ThemeType.VINYL, ThemeType.DEFAULT}


class WidgetConfig(BaseModel):
    theme: ThemeType = ThemeType.DEFAULT
    style: ThemeStyle = ThemeStyle.LIGHT
    color: str | None = None
    spin: bool = False
    eq_color: EqColor = "1ED760"

    @field_validator('color')
    @classmethod
    def validate_color(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.lstrip('#')
        if len(v) not in (3, 6) or not all(c in '0123456789ABCDEFabcdef' for c in v):
            return None  # invalid -> ignore
        return v

    @classmethod
    def from_query_params(
        cls,
        theme: str = "default",
        style: str = "light",
        color: str | None = None,
        spin: bool = False,
        eq_color: str = "1ED760"
    ) -> "WidgetConfig":
        """Create config from URL query parameters."""
        try:
            theme_type = ThemeType(theme.lower())
        except ValueError:
            theme_type = ThemeType.DEFAULT

        # windows98 only supports light style
        if theme_type == ThemeType.WINDOWS98:
            theme_style = ThemeStyle.LIGHT
        else:
            try:
                theme_style = ThemeStyle(style.lower())
            except ValueError:
                theme_style = ThemeStyle.LIGHT

        # color only valid for specific themes
        valid_color = None
        if color and theme_type in COLOR_SUPPORTED_THEMES:
            valid_color = color.lstrip('#')

        return cls(
            theme=theme_type,
            style=theme_style,
            color=valid_color,
            spin=spin,
            eq_color=eq_color
        )
