import hashlib
import time

def generate_short_code(url: str) -> str:
    """Generate a short code for a given URL."""
    unique_string = f"{url}{time.time()}"
    return hashlib.sha256(unique_string.encode()).hexdigest()[:6]
