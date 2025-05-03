import base64
from pathlib import Path
import httpx
from typing import Dict, Optional
from functools import lru_cache


class Base64Encoder:
    """handles image encoding with caching"""
    
    def __init__(self, static_dir: Path):
        """initialize with static directory path"""
        self.static_dir = static_dir
        self._cache: Dict[str, str] = {}
        
    async def encode_url(self, url: str) -> str:
        """encode remote image to base64 with caching"""
        # return from cache if available
        if url in self._cache:
            return self._cache[url]
            
        # fetch and encode remote image
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=3.0)
                if response.status_code == 200:
                    encoded = base64.b64encode(response.content).decode('ascii')
                    # cache for future requests
                    self._cache[url] = encoded
                    return encoded
            except (httpx.RequestError, httpx.TimeoutException):
                pass
                
        # fallback to default placeholder
        return self.get_default_image()
    
    @lru_cache(maxsize=1)    
    def get_default_image(self) -> str:
        """generate placeholder album cover"""
        svg = f'''
        <svg width="120" height="120" xmlns="http://www.w3.org/2000/svg">
            <rect width="120" height="120" fill="#333"/>
            <circle cx="60" cy="60" r="40" fill="#555"/>
            <circle cx="60" cy="60" r="20" fill="#333"/>
            <circle cx="60" cy="60" r="5" fill="#555"/>
        </svg>
        '''
        return base64.b64encode(svg.encode('utf-8')).decode('ascii')
        
    @lru_cache(maxsize=1)
    def get_spotify_logo(self) -> str:
        """get spotify logo from svg file"""
        try:
            svg_path = self.static_dir / "spotify.svg"
            with open(svg_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('ascii')
        except (FileNotFoundError, IOError):
            # minimal spotify logo fallback
            svg = '''
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                <circle cx="12" cy="12" r="12" fill="#1DB954"/>
                <path d="M17.9 10.9c-3.4-2-9-2.2-12.2-1.2-.5.2-1.1-.1-1.3-.6-.2-.5.1-1.1.6-1.3 3.8-1.2 10.1-.9 14 1.4.5.3.7.9.4 1.4-.3.4-.9.6-1.5.3zm-.3 2.9c-.3.4-.8.5-1.2.2-2.8-1.7-7.2-2.2-10.5-1.2-.4.1-.9-.1-1-.5-.1-.4.1-.9.5-1 3.8-1.2 8.7-.6 11.9 1.3.5.3.6.8.3 1.2zm-1.3 2.8c-.3.3-.6.4-1 .2-2.5-1.5-5.6-1.8-9.2-1-.3.1-.7-.1-.8-.5-.1-.3.1-.7.5-.8 4-.9 7.4-.5 10.2 1.2.3.2.4.6.3.9z" fill="white"/>
            </svg>
            '''
            return base64.b64encode(svg.encode('utf-8')).decode('ascii')
        
    @lru_cache(maxsize=1)
    def get_vinyl_overlay(self) -> str:
        """get vinyl overlay from svg file"""
        try:
            svg_path = self.static_dir / "vinyl.svg"
            with open(svg_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('ascii')
        except (FileNotFoundError, IOError):
            # fallback vinyl overlay
            svg = '''
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
            '''
            return base64.b64encode(svg.encode('utf-8')).decode('ascii')
            
    @lru_cache(maxsize=1)
    def get_vinyl_needle(self) -> str:
        """get vinyl needle overlay from svg file"""
        try:
            svg_path = self.static_dir / "vinyl-needle.svg"
            with open(svg_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('ascii')
        except (FileNotFoundError, IOError):
            # fallback vinyl needle overlay
            svg = '''
            <svg width="80" height="120" xmlns="http://www.w3.org/2000/svg">
                <g transform="rotate(-20 40 20)">
                    <rect x="38" y="10" width="4" height="100" fill="#333333" rx="2"/>
                    <circle cx="40" cy="10" r="8" fill="#555555" stroke="#333333" stroke-width="1"/>
                    <rect x="30" y="100" width="20" height="10" fill="#555555" rx="2"/>
                </g>
            </svg>
            '''
            return base64.b64encode(svg.encode('utf-8')).decode('ascii')