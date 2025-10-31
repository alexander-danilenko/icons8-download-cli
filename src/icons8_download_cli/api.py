"""API client for Icons8.com endpoints."""

import logging
from typing import Callable, Optional

import requests

from icons8_download_cli.models import Icon, IconResponse

logger = logging.getLogger(__name__)

API_BASE_URL = "https://api-icons.icons8.com/siteApi/icons/v1/latest"
PAGE_SIZE = 100


def fetch_all_icons(
    style: Optional[str] = None,
    query: Optional[str] = None,
    progress_callback: Optional[Callable[[int], None]] = None,
) -> list[Icon]:
    """
    Fetch all icons from Icons8 API with pagination.

    Args:
        style: Optional style filter
        query: Optional search query term

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
        if query:
            params["term"] = query

        try:
            response = requests.get(API_BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            api_response = IconResponse.model_validate(response.json())

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

