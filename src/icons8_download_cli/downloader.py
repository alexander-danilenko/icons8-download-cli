"""File download and naming conflict resolution."""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Mapping

import requests
from rich.console import Console
from rich.progress import Progress, TaskID

from icons8_download_cli.models import Icon

logger = logging.getLogger(__name__)
console = Console()

DOWNLOAD_BASE_URL = "https://img.icons8.com"


def sanitize_filename(name: str) -> str:
    """
    Sanitize icon name for use as filename.

    Args:
        name: Original icon name

    Returns:
        Sanitized filename-safe string
    """
    # Remove or replace invalid filename characters
    invalid_chars = '<>:"/\\|?*'
    sanitized = name
    for char in invalid_chars:
        sanitized = sanitized.replace(char, "_")
    return sanitized


def resolve_filenames(
    icons: list[Icon],
    target_directory: Path,
) -> Mapping[str, Path]:
    """
    Resolve unique filenames for all icons, checking existing files once.

    Args:
        icons: List of icons to generate filenames for
        target_directory: Directory where icons will be saved

    Returns:
        Mapping of icon.id to final file path
    """
    # Get all existing files in target directory once
    existing_files: set[str] = set()
    if target_directory.exists():
        for file_path in target_directory.iterdir():
            if file_path.is_file():
                existing_files.add(file_path.name.lower())

    filename_map: dict[str, Path] = {}
    name_counts: dict[str, int] = {}

    for icon in icons:
        base_name = sanitize_filename(icon.name)
        base_filename = f"{base_name}.png"

        # Check if base filename exists
        if base_filename.lower() not in existing_files:
            filename_map[icon.id] = target_directory / base_filename
            existing_files.add(base_filename.lower())
        else:
            # Generate unique name with auto-incrementing suffix
            if base_name not in name_counts:
                name_counts[base_name] = 0

            while True:
                name_counts[base_name] += 1
                candidate_name = f"{base_name}({name_counts[base_name]}).png"

                if candidate_name.lower() not in existing_files:
                    filename_map[icon.id] = target_directory / candidate_name
                    existing_files.add(candidate_name.lower())
                    break

    return filename_map


def download_icon(
    icon: Icon,
    file_path: Path,
    size: int,
    progress: Progress,
    task_id: TaskID,
) -> bool:
    """
    Download a single icon to the specified file path.

    Args:
        icon: Icon to download
        file_path: Destination file path
        size: Icon size parameter
        progress: Rich progress bar instance
        task_id: Task ID for progress updates

    Returns:
        True if download succeeded, False otherwise
    """
    download_url = f"{DOWNLOAD_BASE_URL}/?size={size}&id={icon.id}&format=png"

    try:
        response = requests.get(download_url, timeout=30, stream=True)
        response.raise_for_status()

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        progress.update(task_id, advance=1)
        logger.info("Downloaded: %s -> %s", icon.name, file_path.name)
        return True

    except requests.RequestException as e:
        logger.error("Failed to download %s (%s): %s", icon.name, icon.id, e)
        progress.update(task_id, advance=1)
        return False
    except Exception as e:
        logger.error(
            "Unexpected error downloading %s (%s): %s",
            icon.name,
            icon.id,
            e,
        )
        progress.update(task_id, advance=1)
        return False


def download_icons_parallel(
    icons: list[Icon],
    filename_map: Mapping[str, Path],
    size: int,
    progress: Progress,
    task_id: TaskID,
    max_workers: int = 5,
) -> tuple[int, int]:
    """
    Download multiple icons in parallel using thread pool.

    Args:
        icons: List of icons to download
        filename_map: Mapping of icon.id to file path
        size: Icon size parameter
        progress: Rich progress bar instance
        task_id: Task ID for progress updates
        max_workers: Maximum number of concurrent download threads

    Returns:
        Tuple of (successful_count, failed_count)
    """
    downloaded_count = 0
    failed_count = 0

    def download_with_error_handling(icon: Icon) -> bool:
        """Wrapper to handle exceptions in thread pool."""
        file_path = filename_map[icon.id]
        return download_icon(icon, file_path, size, progress, task_id)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all download tasks
        future_to_icon = {
            executor.submit(download_with_error_handling, icon): icon
            for icon in icons
        }

        # Process completed downloads as they finish
        for future in as_completed(future_to_icon):
            icon = future_to_icon[future]
            try:
                success = future.result()
                if success:
                    downloaded_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                logger.error(
                    "Unexpected error in parallel download for %s (%s): %s",
                    icon.name,
                    icon.id,
                    e,
                )
                failed_count += 1

    return downloaded_count, failed_count

