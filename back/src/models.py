"""Data models for the URL shortener service."""

from pydantic import BaseModel, HttpUrl


class URLInput(BaseModel):
    """Input model for URL shortening requests."""

    long_url: HttpUrl


class URLResponse(BaseModel):
    """Response model for shortened URLs."""

    short_url: str
    long_url: str
    expires_in: int  # TTL in seconds
