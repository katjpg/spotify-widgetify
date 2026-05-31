from app.domain import Palette


class ColorService:
    """Derives the text-contrast overlay laid over blurred album art."""

    @staticmethod
    def palette(
        color: str | None,
        is_dark: bool,
        *,
        light_default: str,
        dark_default: str,
        guard_six: bool = False,
    ) -> Palette:
        """Return a Palette whose overlay is derived from a custom hex `color`, else a per-theme
        light/dark default.

        A 6-digit `color` becomes ``rgba(r, g, b, 0.6)``. With `guard_six`, a non-6-digit `color`
        falls back to ``rgba(0,0,0,0.6)``; without it, a short `color` raises (preserved behavior).
        """
        if color:
            hex_digits = color.lstrip("#")
            if guard_six and len(hex_digits) != 6:
                return Palette(overlay="rgba(0,0,0,0.6)")
            r, g, b = (
                int(hex_digits[0:2], 16),
                int(hex_digits[2:4], 16),
                int(hex_digits[4:6], 16),
            )
            return Palette(overlay=f"rgba({r}, {g}, {b}, 0.6)")
        return Palette(overlay=dark_default if is_dark else light_default)
