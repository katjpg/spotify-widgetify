import logging
from datetime import datetime, timedelta
from typing import Any

import httpx

from app.assets.images import ImageEncoder
from app.config import Settings
from app.domain import Track

logger = logging.getLogger(__name__)


class SpotifyAuthClient:
    """Caches a single Spotify access token, refreshing it via the refresh-token grant on expiry."""

    def __init__(self, settings: Settings, http_client: httpx.AsyncClient):
        self.settings = settings
        self.http_client = http_client
        self._token: str | None = None
        self._expires_at: datetime | None = None

    async def get_token(self) -> str:
        """Return a bearer token, refreshing when the cached one expired. Return "" on auth
        failure (logged)."""
        if self._token and self._expires_at and datetime.now() < self._expires_at:
            return self._token

        try:
            response = await self.http_client.post(
                self.settings.auth_api_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.settings.refresh_token.get_secret_value(),
                    "client_id": self.settings.client_id,
                    "client_secret": self.settings.client_secret.get_secret_value(),
                },
                timeout=5.0,
            )

            if response.status_code == 200:
                data = response.json()
                self._token = data["access_token"]
                expires_in = data.get("expires_in", 3600)
                self._expires_at = datetime.now() + timedelta(seconds=expires_in - 60)
                return self._token

            logger.warning(f"Token refresh failed: {response.status_code}")
        except httpx.TimeoutException:
            logger.error("Spotify auth timeout")
        except httpx.RequestError as e:
            logger.error(f"Spotify auth error: {e}")

        return ""


class SpotifyClient:
    """Spotify Web API adapter that returns the now-playing Track."""

    def __init__(
        self,
        auth_client: SpotifyAuthClient,
        settings: Settings,
        encoder: ImageEncoder,
        http_client: httpx.AsyncClient,
    ):
        self.auth_client = auth_client
        self.settings = settings
        self.encoder = encoder
        self.http_client = http_client

    async def fetch_current_track(self) -> Track:
        """Return the currently playing track, else the most recently played, else a not-playing
        fallback."""
        token = await self.auth_client.get_token()
        if not token:
            return self._default_track()

        headers = {"Authorization": f"Bearer {token}"}

        track = await self._fetch_current_track(headers)
        if track:
            return track

        track = await self._fetch_recent_track(headers)
        if track:
            return track

        return self._default_track()

    async def _fetch_current_track(self, headers: dict[str, str]) -> Track | None:
        try:
            response = await self.http_client.get(
                f"{self.settings.spotify_api_url}/me/player/currently-playing",
                headers=headers,
                timeout=5.0,
            )

            if response.status_code == 200 and response.content:
                data = response.json()
                if data.get("item"):
                    return await self._process_track(data["item"], is_playing=True)
        except httpx.TimeoutException:
            logger.warning("Timeout fetching current track")
        except (httpx.RequestError, ValueError) as e:
            logger.warning(f"Error fetching current track: {e}")

        return None

    async def _fetch_recent_track(self, headers: dict[str, str]) -> Track | None:
        try:
            response = await self.http_client.get(
                f"{self.settings.spotify_api_url}/me/player/recently-played?limit=10",
                headers=headers,
                timeout=5.0,
            )

            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                if items:
                    most_recent = max(items, key=lambda x: x.get("played_at", ""))
                    return await self._process_track(
                        most_recent["track"], is_playing=False
                    )

            logger.warning(f"Recent tracks fetch failed: {response.status_code}")
        except httpx.TimeoutException:
            logger.warning("Timeout fetching recent tracks")
        except (httpx.RequestError, ValueError) as e:
            logger.warning(f"Error fetching recent tracks: {e}")

        return None

    async def _process_track(self, item: dict[str, Any], is_playing: bool) -> Track:
        images = item.get("album", {}).get("images", [])
        album_image_url = ""
        if images:
            # prefer the medium image (index 1) over the largest
            album_image_url = images[1]["url"] if len(images) > 1 else images[0]["url"]

        album_art = (
            await self.encoder.encode_url(album_image_url, self.http_client)
            if album_image_url
            else self.encoder.get_default_image()
        )

        return Track.from_spotify_item(item, album_art=album_art, is_playing=is_playing)

    def _default_track(self) -> Track:
        return Track(
            title="Not Playing",
            artist="Spotify",
            album_art=self.encoder.get_default_image(),
            track_id="",
            is_playing=False,
        )
