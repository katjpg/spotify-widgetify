import logging
from datetime import datetime, timedelta

import httpx

from app.config import Settings
from app.utils.base64 import Base64Encoder
from app.domain.models import Track

logger = logging.getLogger(__name__)


class SpotifyAuthClient:
    """Handles Spotify OAuth token management."""

    def __init__(self, settings: Settings, http_client: httpx.AsyncClient):
        self.settings = settings
        self.http_client = http_client
        self._token: str | None = None
        self._expires_at: datetime | None = None

    async def get_token(self) -> str:
        """Get valid access token, refreshing if expired."""
        if self._token and self._expires_at and datetime.now() < self._expires_at:
            return self._token

        try:
            response = await self.http_client.post(
                self.settings.auth_api_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.settings.refresh_token,
                    "client_id": self.settings.client_id,
                    "client_secret": self.settings.client_secret,
                },
                timeout=5.0
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


class SpotifyApiClient:
    """Fetches track data from Spotify API."""

    def __init__(
        self,
        auth_client: SpotifyAuthClient,
        settings: Settings,
        encoder: Base64Encoder,
        http_client: httpx.AsyncClient
    ):
        self.auth_client = auth_client
        self.settings = settings
        self.encoder = encoder
        self.http_client = http_client

    async def get_current_track(self) -> Track:
        """Get currently playing or most recently played track."""
        token = await self.auth_client.get_token()
        if not token:
            return self._get_default_track()

        headers = {"Authorization": f"Bearer {token}"}

        track = await self._fetch_current_track(headers)
        if track:
            return track

        track = await self._fetch_recent_track(headers)
        if track:
            return track

        return self._get_default_track()

    async def _fetch_current_track(self, headers: dict[str, str]) -> Track | None:
        try:
            response = await self.http_client.get(
                f"{self.settings.spotify_api_url}/me/player/currently-playing",
                headers=headers,
                timeout=5.0
            )

            if response.status_code == 200 and response.content:
                data = response.json()
                if data.get('item'):
                    return await self._process_track(data['item'])
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
                timeout=5.0
            )

            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                if items:
                    # sort by played_at desc, get most recent
                    sorted_items = sorted(
                        items,
                        key=lambda x: x.get('played_at', ''),
                        reverse=True
                    )
                    return await self._process_track(sorted_items[0]['track'])

            logger.warning(f"Recent tracks fetch failed: {response.status_code}")
        except httpx.TimeoutException:
            logger.warning("Timeout fetching recent tracks")
        except (httpx.RequestError, ValueError) as e:
            logger.warning(f"Error fetching recent tracks: {e}")

        return None

    async def _process_track(self, track_data: dict) -> Track:
        """Transform Spotify API response into Track model."""
        album_image_url = ""
        images = track_data.get('album', {}).get('images', [])
        if images:
            album_image_url = images[1]['url'] if len(images) > 1 else images[0]['url']

        album_image = (
            await self.encoder.encode_url(album_image_url)
            if album_image_url
            else self.encoder.get_default_image()
        )

        artists = track_data.get('artists', [{}])
        artist_name = artists[0].get('name', 'Unknown Artist') if artists else 'Unknown Artist'

        return Track(
            name=track_data.get('name', 'Unknown Track'),
            artist=artist_name,
            album_image=album_image,
            uri=track_data.get('uri', ''),
            id=track_data.get('id', '')
        )

    def _get_default_track(self) -> Track:
        return Track(
            name='Not Playing',
            artist='Spotify',
            album_image=self.encoder.get_default_image(),
            uri='',
            id=''
        )
