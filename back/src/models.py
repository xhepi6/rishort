from pydantic import BaseModel, HttpUrl

class URLInput(BaseModel):
    long_url: HttpUrl

class URLResponse(BaseModel):
    short_url: str
    long_url: str
    expires_in: int  # TTL in seconds
