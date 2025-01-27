"""URL routing and endpoint handlers for the URL shortener service."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from .models import URLInput, URLResponse
from .services import URLShortenerService

router = APIRouter()
url_service = URLShortenerService()


@router.post("/shorten", response_model=URLResponse)
async def create_short_url(url_input: URLInput, request: Request):
    """Create a shortened URL from a long URL.

    Args:
        url_input: The input URL to be shortened
        request: The FastAPI request object

    Returns:
        URLResponse: The shortened URL response object
    """
    return url_service.create_short_url(str(url_input.long_url), str(request.base_url))


@router.get("/{short_code}")
async def redirect_to_url(short_code: str):
    """Redirect to the original URL from a short code.

    Args:
        short_code: The short code to look up

    Returns:
        RedirectResponse: Redirect to the original URL

    Raises:
        HTTPException: If the URL is not found
    """
    long_url = url_service.get_long_url(short_code)
    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=long_url)


@router.get("/")
async def root():
    """Get API health status and version information.

    Returns:
        dict: Health check response containing status and version
    """
    return {"status": "healthy", "service": "URL Shortener", "version": "1.0.0"}
