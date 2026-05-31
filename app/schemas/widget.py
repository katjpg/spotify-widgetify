from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from app.domain import ThemeName, ThemeStyle, WidgetConfig

# custom colors apply only to themes whose surface they can recolor coherently
COLOR_SUPPORTED_THEMES = {ThemeName.IPOD, ThemeName.VINYL, ThemeName.DEFAULT}

_HEX = set("0123456789ABCDEFabcdef")


def _validate_eq_color(value: str) -> str:
    """Accept "rainbow"/"none" (case-insensitive) or a 3/6-digit hex; raise on anything else."""
    if value.lower() in ("rainbow", "none"):
        return value.lower()
    digits = value.lstrip("#")
    if len(digits) not in (3, 6) or not all(c in _HEX for c in digits):
        raise ValueError("Invalid hex color")
    return digits


EqColor = Annotated[str, AfterValidator(_validate_eq_color)]


class WidgetParams(BaseModel):
    theme: str = "default"
    style: str = "light"
    color: str | None = Field(default=None, pattern=r"^[0-9A-Fa-f]{3,6}$")
    eq_color: EqColor = "1ED760"
    # legacy aliases; when present they take precedence over theme/style
    theme_type: str | None = None
    theme_style: str | None = None


def build_config(params: WidgetParams) -> WidgetConfig:
    """Map validated query params to a WidgetConfig: resolve enums, force windows98 to light, and
    keep a custom color only for the themes that support it."""
    theme_name = (params.theme_type or params.theme).lower()
    try:
        theme = ThemeName(theme_name)
    except ValueError:
        theme = ThemeName.DEFAULT

    if theme is ThemeName.WINDOWS98:
        style = ThemeStyle.LIGHT
    else:
        try:
            style = ThemeStyle((params.theme_style or params.style).lower())
        except ValueError:
            style = ThemeStyle.LIGHT

    color = None
    if params.color and theme in COLOR_SUPPORTED_THEMES:
        color = params.color.lstrip("#")

    return WidgetConfig(theme=theme, style=style, color=color, eq_color=params.eq_color)
