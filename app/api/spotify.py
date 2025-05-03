import httpx
from typing import Dict, Any, Optional
from app.config import Settings
from app.utils.base64 import Base64Encoder
from app.domain.models import Track, ThemeStyle


class SpotifyAuthClient:
    """handles spotify api authentication"""
    
    def __init__(self, settings: Settings):
        """initialize with application settings"""
        self.settings = settings
        self._token: Optional[str] = None
        
    async def get_token(self) -> str:
        """get access token using refresh token flow"""
        # return cached token if available
        if self._token:
            return self._token
            
        # request new token
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
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
                    return self._token
            except (httpx.RequestError, httpx.TimeoutException):
                pass
                
        # fallback to empty token
        return ""


class SpotifyApiClient:
    """handles spotify api data access"""
    
    def __init__(self, auth_client: SpotifyAuthClient, settings: Settings, encoder: Base64Encoder):
        """initialize with required dependencies"""
        self.auth_client = auth_client
        self.settings = settings
        self.encoder = encoder
        self.timeout = 5.0  # request timeout in seconds
        
    async def get_current_track(self) -> Track:
        """get user's currently playing or recently played track"""
        token = await self.auth_client.get_token()
        if not token:
            return self._get_default_track()
            
        headers = {"Authorization": f"Bearer {token}"}
        
        # try current track first, then fall back to recent
        current = await self._fetch_current_track(headers)
        if current:
            return current
            
        recent = await self._fetch_recent_track(headers)
        if recent:
            return recent
            
        # final fallback
        return self._get_default_track()
    
    async def _fetch_current_track(self, headers: Dict[str, str]) -> Optional[Track]:
        """fetch currently playing track from api"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.settings.spotify_api_url}/me/player/currently-playing",
                    headers=headers,
                    timeout=self.timeout
                )
                
                if response.status_code == 200 and response.content:
                    data = response.json()
                    if data.get('item'):
                        return await self._process_track(data['item'])
            except (httpx.RequestError, httpx.TimeoutException, ValueError):
                pass
                
        return None
        
    async def _fetch_recent_track(self, headers: Dict[str, str]) -> Optional[Track]:
        """fetch recently played track from api, ensuring we get the most recent by timestamp"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.settings.spotify_api_url}/me/player/recently-played?limit=10",
                    headers=headers,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('items') and len(data['items']) > 0:
                        sorted_items = sorted(
                            data['items'], 
                            key=lambda item: item.get('played_at', ''), 
                            reverse=True 
                        )
                        return await self._process_track(sorted_items[0]['track'])
                print(f"Failed to fetch recent track, status: {response.status_code}")
            except (httpx.RequestError, httpx.TimeoutException, ValueError) as e:
                print(f"Error fetching recent track: {str(e)}")
                pass
                    
        return None
    
    async def _process_track(self, track_data: Dict[str, Any]) -> Track:
        """process api track data into domain model"""
        # extract album image url
        album_image_url = ""
        if (track_data.get('album') and 
                track_data['album'].get('images') and 
                len(track_data['album']['images']) > 0):
            # prefer medium size image
            album_image_url = (track_data['album']['images'][1]['url'] 
                              if len(track_data['album']['images']) > 1 
                              else track_data['album']['images'][0]['url'])
        
        # get base64 encoded image
        album_image = await self.encoder.encode_url(album_image_url) if album_image_url else self.encoder.get_default_image()
        
        # build track domain object
        return Track(
            name=track_data.get('name', 'Unknown Track'),
            artist=track_data.get('artists', [{}])[0].get('name', 'Unknown Artist'),
            album_image=album_image,
            uri=track_data.get('uri', ''),
            id=track_data.get('id', '')
        )
        
    def _get_default_track(self) -> Track:
        """create fallback track when no data available"""
        return Track(
            name='Not Playing',
            artist='Spotify',
            album_image=self.encoder.get_default_image(),
            uri='',
            id=''
        )