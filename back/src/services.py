"""Service layer for URL shortening functionality."""

from typing import Optional

import redis

from .models import URLResponse
from .settings import get_settings
from .utils import generate_short_code


class URLShortenerService:
    """Service class for handling URL shortening operations."""

    _instance = None
    TTL = 86400  # 24 hours in seconds

    def __new__(cls):
        """Create a singleton instance of the service."""
        if cls._instance is None:
            cls._instance = super(URLShortenerService, cls).__new__(cls)
            settings = get_settings()
            cls._instance._redis = redis.Redis.from_url(
                settings.REDIS_URL, decode_responses=True
            )
        return cls._instance

    def create_short_url(self, long_url: str, base_url: str) -> URLResponse:
        """Create a shortened URL and store the mapping."""
        short_code = generate_short_code(long_url)

        # Store in Redis with an expiry of 24 hours
        self._redis.setex(short_code, self.TTL, long_url)

        short_url = f"{base_url}{short_code}"
        return URLResponse(short_url=short_url, long_url=long_url, expires_in=self.TTL)

    def get_long_url(self, short_code: str) -> Optional[str]:
        """Retrieve the original URL from a short code."""
        return self._redis.get(short_code)
