"""API client for Icons8.com endpoints."""

import logging
from typing import Callable, Optional

import requests

from icons8_download_cli.cache import read_cache, write_cache
from icons8_download_cli.models import Icon, IconResponse

logger = logging.getLogger(__name__)

API_BASE_URL = "https://api-icons.icons8.com/siteApi/icons/v1/latest"
PAGE_SIZE = 100


def fetch_all_icons(
    style: Optional[str] = None,
    progress_callback: Optional[Callable[[int], None]] = None,
    use_cache: bool = True,
) -> list[Icon]:
    """
    Fetch all icons from Icons8 API with pagination.

    Args:
        style: Optional style filter
        progress_callback: Optional callback function for progress updates
        use_cache: Whether to use cached responses (default: True)

    Returns:
        List of all Icon objects collected across all pages

    Raises:
        requests.RequestException: If API request fails
    """
    all_icons: list[Icon] = []
    offset = 0

    while True:
        params = {
            "amount": PAGE_SIZE,
            "offset": offset,
            "ai": "true",
            "language": "en-US",
            "sortBy": "mostDownloaded",
        }

        if style:
            params["style"] = style

        # Construct full URL for cache key
        prepared_request = requests.PreparedRequest()
        prepared_request.prepare_url(API_BASE_URL, params)
        full_url = prepared_request.url or API_BASE_URL

        try:
            # Check cache first
            cached_data = None
            if use_cache:
                cached_data = read_cache(full_url)

            if cached_data:
                logger.info("API request (cache hit): %s", full_url)
                api_response = IconResponse.model_validate(cached_data)
            else:
                if use_cache:
                    logger.info("API request (cache miss): %s", full_url)
                else:
                    logger.info("API request: %s", full_url)
                response = requests.get(API_BASE_URL, params=params, timeout=30)
                response.raise_for_status()
                response_json = response.json()

                # Cache the response
                if use_cache:
                    write_cache(full_url, response_json)

                api_response = IconResponse.model_validate(response_json)

            if not api_response.success:
                logger.warning(
                    "API returned non-success response at offset %d",
                    offset,
                )
                break

            if not api_response.icons:
                logger.info("No more icons found at offset %d", offset)
                break

            all_icons.extend(api_response.icons)

            # Update progress if callback provided
            if progress_callback:
                progress_callback(len(all_icons))

            # If we got fewer icons than requested, we've reached the end
            if len(api_response.icons) < PAGE_SIZE:
                break

            offset += PAGE_SIZE

        except requests.RequestException as e:
            logger.error("Failed to fetch icons at offset %d: %s", offset, e)
            raise
        except Exception as e:
            logger.error(
                "Unexpected error processing API response at offset %d: %s",
                offset,
                e,
            )
            raise

    return all_icons

