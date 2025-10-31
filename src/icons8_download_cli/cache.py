"""Cache utilities for API response caching."""

import hashlib
import json
import logging
import tempfile
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


def get_cache_dir() -> Path:
    """
    Get the cache directory path.

    Returns:
        Path to icons8 directory in system temp directory
    """
    temp_dir = Path(tempfile.gettempdir())
    cache_dir = temp_dir / "icons8"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def generate_cache_key(url: str) -> str:
    """
    Generate cache key from URL string.

    Args:
        url: Full GET URL string (base URL + query params)

    Returns:
        SHA256 hash of the URL as hex string
    """
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def get_cache_path(url: str) -> Path:
    """
    Get the cache file path for a given URL.

    Args:
        url: Full GET URL string

    Returns:
        Path to cache file
    """
    cache_key = generate_cache_key(url)
    cache_dir = get_cache_dir()
    return cache_dir / f"{cache_key}.json"


def read_cache(url: str) -> Optional[dict[str, Any]]:
    """
    Read cached response for a given URL.

    Args:
        url: Full GET URL string

    Returns:
        Cached response data as dict, or None if not found or invalid
    """
    cache_path = get_cache_path(url)

    if not cache_path.exists():
        return None

    try:
        with cache_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug("Cache hit for URL: %s", url)
        return data
    except (json.JSONDecodeError, IOError) as e:
        logger.warning("Failed to read cache file %s: %s", cache_path, e)
        return None


def write_cache(url: str, response_data: dict[str, Any]) -> None:
    """
    Write response data to cache.

    Args:
        url: Full GET URL string
        response_data: Response data to cache (dict)
    """
    cache_path = get_cache_path(url)

    try:
        with cache_path.open("w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=2)
        logger.debug("Cached response for URL: %s", url)
    except IOError as e:
        logger.warning("Failed to write cache file %s: %s", cache_path, e)

