import base64
import logging
from collections import OrderedDict
from functools import lru_cache
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

_DEFAULT_IMAGE_SVG = """
        <svg width="120" height="120" xmlns="http://www.w3.org/2000/svg">
            <rect width="120" height="120" fill="#333"/>
            <circle cx="60" cy="60" r="40" fill="#555"/>
            <circle cx="60" cy="60" r="20" fill="#333"/>
            <circle cx="60" cy="60" r="5" fill="#555"/>
        </svg>
        """

_SPOTIFY_LOGO_FALLBACK_SVG = """
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                <circle cx="12" cy="12" r="12" fill="#1DB954"/>
                <path d="M17.9 10.9c-3.4-2-9-2.2-12.2-1.2-.5.2-1.1-.1-1.3-.6-.2-.5.1-1.1.6-1.3 3.8-1.2 10.1-.9 14 1.4.5.3.7.9.4 1.4-.3.4-.9.6-1.5.3zm-.3 2.9c-.3.4-.8.5-1.2.2-2.8-1.7-7.2-2.2-10.5-1.2-.4.1-.9-.1-1-.5-.1-.4.1-.9.5-1 3.8-1.2 8.7-.6 11.9 1.3.5.3.6.8.3 1.2zm-1.3 2.8c-.3.3-.6.4-1 .2-2.5-1.5-5.6-1.8-9.2-1-.3.1-.7-.1-.8-.5-.1-.3.1-.7.5-.8 4-.9 7.4-.5 10.2 1.2.3.2.4.6.3.9z" fill="white"/>
            </svg>
            """

_VINYL_OVERLAY_FALLBACK_SVG = """
            <svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
                <circle cx="100" cy="100" r="95" fill="#000000"/>
                <circle cx="100" cy="100" r="30" fill="#171717"/>
                <circle cx="100" cy="100" r="5" fill="#000000"/>
                <circle cx="100" cy="100" r="80" fill="none" stroke="#333" stroke-width="1"/>
                <circle cx="100" cy="100" r="70" fill="none" stroke="#333" stroke-width="1"/>
                <circle cx="100" cy="100" r="60" fill="none" stroke="#333" stroke-width="1"/>
                <circle cx="100" cy="100" r="50" fill="none" stroke="#333" stroke-width="1"/>
                <circle cx="100" cy="100" r="40" fill="none" stroke="#333" stroke-width="1"/>
            </svg>
            """

_VINYL_NEEDLE_FALLBACK_SVG = """
            <svg width="80" height="120" xmlns="http://www.w3.org/2000/svg">
                <g transform="rotate(-20 40 20)">
                    <rect x="38" y="10" width="4" height="100" fill="#333333" rx="2"/>
                    <circle cx="40" cy="10" r="8" fill="#555555" stroke="#333333" stroke-width="1"/>
                    <rect x="30" y="100" width="20" height="10" fill="#555555" rx="2"/>
                </g>
            </svg>
            """


def _encode(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


class ImageEncoder:
    """Encodes images to base64, caching remote fetches (LRU) and bundled static assets."""

    def __init__(self, static_dir: Path, max_cache_size: int = 100):
        self.static_dir = static_dir
        self._cache: OrderedDict[str, str] = OrderedDict()
        self.max_cache_size = max_cache_size

    async def encode_url(self, url: str, http_client: httpx.AsyncClient) -> str:
        """Fetch `url` and return its base64 body, caching by url. Return the default image on
        timeout or transport error (logged)."""
        if url in self._cache:
            self._cache.move_to_end(url)
            return self._cache[url]

        try:
            response = await http_client.get(url, timeout=3.0)
            if response.status_code == 200:
                encoded = _encode(response.content)
                self._add_to_cache(url, encoded)
                return encoded
        except httpx.TimeoutException:
            logger.warning(f"Timeout fetching image: {url}")
        except httpx.RequestError as e:
            logger.warning(f"Error fetching image: {e}")

        return self.get_default_image()

    def _add_to_cache(self, url: str, encoded: str) -> None:
        if len(self._cache) >= self.max_cache_size:
            self._cache.popitem(last=False)  # evict oldest
        self._cache[url] = encoded

    def _encode_asset(self, filename: str, fallback_svg: str) -> str:
        """Encode static_dir/filename, falling back to an inline SVG when the file is absent."""
        try:
            return _encode((self.static_dir / filename).read_bytes())
        except (FileNotFoundError, IOError):
            return _encode(fallback_svg.encode("utf-8"))

    @lru_cache(maxsize=1)
    def get_default_image(self) -> str:
        return _encode(_DEFAULT_IMAGE_SVG.encode("utf-8"))

    @lru_cache(maxsize=1)
    def get_spotify_logo(self) -> str:
        return self._encode_asset("spotify.svg", _SPOTIFY_LOGO_FALLBACK_SVG)

    @lru_cache(maxsize=1)
    def get_vinyl_overlay(self) -> str:
        return self._encode_asset("vinyl.svg", _VINYL_OVERLAY_FALLBACK_SVG)

    @lru_cache(maxsize=1)
    def get_vinyl_needle(self) -> str:
        return self._encode_asset("vinyl-needle.svg", _VINYL_NEEDLE_FALLBACK_SVG)
