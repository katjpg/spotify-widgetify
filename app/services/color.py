import colorsys
import logging
from io import BytesIO

from PIL import Image

from app.domain import FALLBACK_PALETTE, Palette

logger = logging.getLogger(__name__)

TEXT_LIGHT = "#FFFFFF"
TEXT_DARK = "#1B1B1B"

VIBRANT_SATURATION = 0.5  # min saturation to count as vibrant
VIBRANT_SHARE = 0.15  # ...and min share of the cover to win


def _rgb_str(rgb: tuple[int, int, int]) -> str:
    return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"


def _parse_rgb(color: str) -> tuple[int, int, int]:
    value = color.strip()
    if value.startswith("rgb"):
        parts = value[value.index("(") + 1 : value.index(")")].split(",")
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    digits = value.lstrip("#")
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    return (int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16))


def _relative_luminance(r: int, g: int, b: int) -> float:
    def channel(c: int) -> float:
        cs = c / 255
        return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _text_token(r: int, g: int, b: int) -> str:
    return TEXT_DARK if _relative_luminance(r, g, b) > 0.5 else TEXT_LIGHT


def _saturation(r: int, g: int, b: int) -> float:
    mx, mn = max(r, g, b), min(r, g, b)
    return 0.0 if mx == 0 else (mx - mn) / mx


def _from_hls(h: float, lt: float, s: float) -> tuple[int, int, int]:
    return tuple(round(c * 255) for c in colorsys.hls_to_rgb(h, lt, s))


def _vibrance_score(rgb: tuple[int, int, int], population: int, total: int) -> float:
    """Rank a vibrant swatch by saturation, mid-luminance, and population share."""
    lum_target = 1 - abs(_relative_luminance(*rgb) - 0.5) * 2
    return _saturation(*rgb) * 0.5 + lum_target * 0.2 + (population / total) * 0.3


def _pick(
    swatches: list[tuple[int, tuple[int, int, int]]], total: int
) -> tuple[int, int, int]:
    """Pick the album color: a vibrant accent only if also prominent, else the dominant tone."""
    vibrant = [
        (pop, rgb)
        for pop, rgb in swatches
        if _saturation(*rgb) >= VIBRANT_SATURATION and pop / total >= VIBRANT_SHARE
    ]
    if vibrant:
        return max(vibrant, key=lambda x: _vibrance_score(x[1], x[0], total))[1]
    return max(swatches, key=lambda x: x[0])[
        1
    ]  # most populous swatch (the muted dominant)


class ColorService:
    """Derives the album's representative color and the widget text token."""

    @staticmethod
    def extract_palette(image_bytes: bytes) -> Palette:
        """Population-gated vibrant->muted->dominant pick; text contrasts the rendered field.

        Deterministic; returns FALLBACK_PALETTE on undecodable bytes.
        """
        try:
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
            image.thumbnail((300, 300))
            quantized = image.quantize(
                colors=16, method=Image.Quantize.MEDIANCUT
            ).convert("RGB")
            swatches = quantized.getcolors(65536)  # (population, rgb) pairs
        except Exception as e:
            logger.warning(f"Palette extraction failed, using fallback: {e}")
            return FALLBACK_PALETTE

        if not swatches:
            return FALLBACK_PALETTE

        total = sum(pop for pop, _ in swatches)
        winner = _pick(swatches, total)

        h, lt, s = colorsys.rgb_to_hls(*(c / 255 for c in winner))
        l_primary = min(0.42, max(0.26, lt))
        primary = _from_hls(h, l_primary, s)
        secondary = _from_hls(h, max(0.18, l_primary - 0.14), s)

        # text contrasts the blurred field ~ the cover average, after the frost and dark wash
        avg = tuple(
            round(sum(pop * rgb[i] for pop, rgb in swatches) / total) for i in range(3)
        )
        frosted = tuple(round(c * 0.94 + 255 * 0.06) for c in avg)
        field = tuple(round(c * 0.84) for c in frosted)
        return Palette(
            primary=_rgb_str(primary),
            secondary=_rgb_str(secondary),
            text=_text_token(*field),
        )

    @staticmethod
    def text_for(color: str) -> str:
        """Return the light/dark text token contrasting a flat background color (hex or rgb())."""
        try:
            return _text_token(*_parse_rgb(color))
        except (ValueError, IndexError):
            return TEXT_LIGHT
