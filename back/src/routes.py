from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from .models import URLInput, URLResponse
from .services import URLShortenerService

router = APIRouter()
url_service = URLShortenerService()

@router.post("/shorten", response_model=URLResponse)
async def create_short_url(url_input: URLInput, request: Request):
    """Create a shortened URL from a long URL."""
    return url_service.create_short_url(
        str(url_input.long_url),
        str(request.base_url)
    )

@router.get("/{short_code}")
async def redirect_to_url(short_code: str):
    """Redirect to the original URL from a short code."""
    long_url = url_service.get_long_url(short_code)
    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=long_url)

@router.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "URL Shortener",
        "version": "1.0.0"
    }
