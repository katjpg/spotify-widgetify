from typing import Any, Mapping

from dataclasses import dataclass, field

from app.domain.theme import FALLBACK_PALETTE, Palette


@dataclass(frozen=True, slots=True)
class Track:
    title: str = "Not Playing"
    artist: str = ""
    album_art: str = ""  # base64-encoded image, ready for the template
    track_id: str = ""
    is_playing: bool = False
    palette: Palette = field(default=FALLBACK_PALETTE)  # colors derived from album_art

    @classmethod
    def from_spotify_item(
        cls,
        item: Mapping[str, Any],
        album_art: str,
        is_playing: bool,
        palette: Palette,
    ) -> "Track":
        """Map an already-fetched Spotify track item to a Track. No HTTP or encoding here."""
        artists = item.get("artists") or [{}]
        return cls(
            title=item.get("name", "Unknown Track"),
            artist=artists[0].get("name", "Unknown Artist"),
            album_art=album_art,
            track_id=item.get("id", ""),
            is_playing=is_playing,
            palette=palette,
        )
