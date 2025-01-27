import pytest
from fakeredis import FakeRedis
from fastapi.testclient import TestClient
from main import app
from src.services import URLShortenerService
from src.utils import generate_short_code


# Fixtures
@pytest.fixture
def client():
    """Fixture for FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def fake_redis():
    """Fixture for fake Redis."""
    return FakeRedis(decode_responses=True)


@pytest.fixture
def url_service(fake_redis):
    """Fixture for URL shortener service with fake Redis."""
    service = URLShortenerService()
    service._redis = fake_redis
    return service


@pytest.fixture
def test_url():
    """Fixture for test URL"""
    return "https://example.com/very/long/url"


@pytest.fixture
def base_url():
    """Fixture for base URL"""
    return "http://localhost/"


@pytest.fixture
def short_url(client, url_service, test_url):
    """Fixture that creates and returns a short URL"""
    response = client.post("/shorten", json={"long_url": test_url})
    return response.json()["short_url"]


# Health Check Tests
def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "URL Shortener"


# URL Shortening Tests
def test_create_short_url(client, url_service, test_url):
    """Test URL shortening endpoint."""
    response = client.post("/shorten", json={"long_url": test_url})
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == test_url
    assert "short_url" in data
    assert len(data["short_url"]) > len("http://")


def test_invalid_url_input(client):
    """Test handling of invalid URL input."""
    response = client.post("/shorten", json={"long_url": "not-a-valid-url"})
    assert response.status_code == 422


# URL Redirection Tests
def test_redirect_to_url(client, url_service, test_url, short_url):
    """Test URL redirection."""
    short_code = short_url.split("/")[-1]

    # Test redirection
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == test_url


def test_invalid_short_url(client, url_service):
    """Test handling of invalid short URLs."""
    response = client.get("/invalid123", follow_redirects=False)
    assert response.status_code == 404


# URL Service Tests
def test_short_code_generation(test_url):
    """Test generation of short codes."""
    code1 = generate_short_code(test_url)
    code2 = generate_short_code(test_url)
    assert len(code1) == 6
    assert code1 != code2  # Should be different due to timestamp


def test_url_service_operations(url_service, test_url, base_url):
    """Test URL service creation and retrieval operations."""
    # Test URL creation
    response = url_service.create_short_url(test_url, base_url)
    assert response.long_url == test_url
    assert response.short_url.startswith(base_url)

    # Test URL retrieval
    short_code = response.short_url.split("/")[-1]
    retrieved_url = url_service.get_long_url(short_code)
    assert retrieved_url == test_url


# CORS Tests
def test_cors_headers(client):
    """Test CORS headers are properly set."""
    headers = {
        "origin": "http://localhost:3000",
        "access-control-request-method": "POST",
        "access-control-request-headers": "content-type",
    }
    response = client.options("/shorten", headers=headers)
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "access-control-allow-methods" in response.headers
    assert "POST" in response.headers["access-control-allow-methods"]
