"""CLI entry point and command definitions."""

import logging
import os
import platform
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

from icons8_download_cli.api import fetch_all_icons
from icons8_download_cli.downloader import download_icons_parallel, resolve_filenames
from icons8_download_cli.models import Icon

console = Console()

# Size choices enum
SIZE_CHOICES = click.Choice(["24", "48", "96", "192", "384", "512"], case_sensitive=False)


def get_default_downloads_dir() -> Path:
    """
    Get OS-specific Downloads directory respecting non-standard paths.

    Handles:
    - Windows: Uses Windows API to get actual Downloads folder location
    - Linux: Checks XDG_DOWNLOAD_DIR environment variable, falls back to ~/Downloads
    - macOS: Uses ~/Downloads (standard location, can be overridden in Finder)

    Returns:
        Path to Downloads directory
    """
    system = platform.system()

    if system == "Windows":
        downloads_dir = _get_windows_downloads_dir()
    elif system == "Linux":
        downloads_dir = _get_linux_downloads_dir()
    elif system == "Darwin":  # macOS
        downloads_dir = _get_macos_downloads_dir()
    else:
        # Fallback for unknown systems
        downloads_dir = Path.home() / "Downloads"

    downloads_dir.mkdir(parents=True, exist_ok=True)
    return downloads_dir


def _get_windows_downloads_dir() -> Path:
    """
    Get Windows Downloads directory using Windows API.

    Uses SHGetKnownFolderPath with FOLDERID_Downloads to get the actual
    Downloads folder location, even if it's been moved from default.

    Returns:
        Path to Downloads directory
    """
    try:
        import ctypes
        from ctypes import wintypes

        # FOLDERID_Downloads GUID: {374DE290-123F-4565-9164-39C4925E467B}
        # Create GUID structure
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", ctypes.c_byte * 8),
            ]

        # Parse GUID string into GUID structure
        guid_str = "{374DE290-123F-4565-9164-39C4925E467B}"
        guid = GUID()
        guid.Data1 = int(guid_str[1:9], 16)
        guid.Data2 = int(guid_str[10:14], 16)
        guid.Data3 = int(guid_str[15:19], 16)
        guid.Data4[0] = int(guid_str[20:22], 16)
        guid.Data4[1] = int(guid_str[22:24], 16)
        for i in range(2, 8):
            guid.Data4[i] = int(guid_str[25 + (i - 2) * 2 : 27 + (i - 2) * 2], 16)

        # Load shell32.dll and ole32.dll
        shell32 = ctypes.windll.shell32
        ole32 = ctypes.windll.ole32

        # Define SHGetKnownFolderPath function signature
        shell32.SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(GUID),  # rfid (GUID pointer)
            wintypes.DWORD,        # dwFlags
            wintypes.HANDLE,       # hToken
            ctypes.POINTER(ctypes.c_wchar_p),  # ppszPath
        ]
        shell32.SHGetKnownFolderPath.restype = wintypes.HRESULT

        # Call SHGetKnownFolderPath
        path_ptr = ctypes.c_wchar_p()
        result = shell32.SHGetKnownFolderPath(
            ctypes.byref(guid),
            0,
            None,
            ctypes.byref(path_ptr),
        )

        if result == 0:  # S_OK
            downloads_path = path_ptr.value
            ole32.CoTaskMemFree(path_ptr)
            if downloads_path:
                return Path(downloads_path)

    except (OSError, AttributeError, ValueError, ImportError):
        # Fallback if Windows API fails or ctypes not available
        pass

    # Fallback to default location
    return Path.home() / "Downloads"


def _get_linux_downloads_dir() -> Path:
    """
    Get Linux Downloads directory respecting XDG user directories.

    Checks XDG_DOWNLOAD_DIR environment variable first, then falls back
    to ~/Downloads per XDG Base Directory Specification.

    Returns:
        Path to Downloads directory
    """
    # Check XDG_DOWNLOAD_DIR environment variable
    xdg_download_dir = os.environ.get("XDG_DOWNLOAD_DIR")
    if xdg_download_dir:
        return Path(xdg_download_dir)

    # Fallback to default location
    return Path.home() / "Downloads"


def _get_macos_downloads_dir() -> Path:
    """
    Get macOS Downloads directory.

    On macOS, the Downloads folder is typically ~/Downloads, but users
    can move it in Finder. This function uses the standard location.

    Returns:
        Path to Downloads directory
    """
    return Path.home() / "Downloads"


def setup_file_logging(target_directory: Path) -> None:
    """
    Setup file logging to target directory.

    Args:
        target_directory: Directory where log file will be created
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = target_directory / f"icons8-download-log-{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )

    logger = logging.getLogger(__name__)
    logger.info("Logging initialized. Log file: %s", log_file)


@click.command()
@click.option(
    "--target-directory",
    "-d",
    type=click.Path(exists=False, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Target directory for downloaded icons (defaults to Downloads)",
)
@click.option(
    "--size",
    "-s",
    type=SIZE_CHOICES,
    default="512",
    help="Icon size (default: 512)",
)
@click.option(
    "--style",
    "-S",
    type=str,
    default=None,
    help="Icon style filter",
)
@click.option(
    "--query",
    "-q",
    type=str,
    default=None,
    help="Search query term (required if style is not provided)",
)
@click.option(
    "--workers",
    "-w",
    type=int,
    default=10,
    help="Number of parallel download threads (default: 10)",
)
@click.option(
    "--no-cache",
    "-C",
    is_flag=True,
    default=False,
    help="Disable response caching",
)
def download(
    target_directory: Path | None,
    size: str,
    style: str | None,
    query: str | None,
    workers: int,
    no_cache: bool,
) -> None:
    """
    Download icons from Icons8.com API.

    Either --style or --query must be provided.
    """
    # Determine target directory
    if target_directory is None:
        target_directory = get_default_downloads_dir()
    else:
        target_directory = Path(target_directory).resolve()
        target_directory.mkdir(parents=True, exist_ok=True)

    # Validate that either style or query is provided
    if not style and not query:
        console.print(
            "[red]Error:[/red] Either --style or --query must be provided",
        )
        raise click.Abort()

    # Setup logging
    setup_file_logging(target_directory)

    logger = logging.getLogger(__name__)
    logger.info("Starting download to: %s", target_directory)
    logger.info(
        "Parameters: size=%s, style=%s, query=%s, workers=%s",
        size,
        style,
        query,
        workers,
    )

    console.print(f"\n[bold]Icons8 Download CLI[/bold]")
    console.print(f"Target directory: [cyan]{target_directory}[/cyan]")
    console.print(f"Size: [cyan]{size}[/cyan]px")
    if style:
        console.print(f"Style: [cyan]{style}[/cyan]")
    if query:
        console.print(f"Query: [cyan]{query}[/cyan]")
    console.print(f"Parallel workers: [cyan]{workers}[/cyan]")
    console.print()

    # Fetch all icons with progress
    console.print("[yellow]Collecting icons...[/yellow]")
    all_icons: list[Icon] = []
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Fetching icons from API...", total=None)

            def update_progress(count: int) -> None:
                progress.update(
                    task,
                    description=f"Fetching icons from API... ({count} found)",
                )

            all_icons = fetch_all_icons(
                style=style,
                query=query,
                progress_callback=update_progress,
                use_cache=not no_cache,
            )
            progress.update(
                task,
                description=f"Found {len(all_icons)} icons",
            )

        console.print(f"[green]✓[/green] Found [bold]{len(all_icons)}[/bold] icons\n")

    except Exception as e:
        console.print(f"[red]✗[/red] Failed to fetch icons: {e}")
        logger.exception("Failed to fetch icons")
        raise click.Abort()

    if not all_icons:
        console.print("[yellow]No icons found. Exiting.[/yellow]")
        return

    # Resolve filenames
    console.print("[yellow]Resolving filenames...[/yellow]")
    filename_map = resolve_filenames(all_icons, target_directory)
    console.print(f"[green]✓[/green] Resolved {len(filename_map)} filenames\n")

    # Download icons with progress (parallel)
    console.print("[yellow]Downloading icons...[/yellow]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        console=console,
    ) as progress:
        task = progress.add_task(
            "Downloading...",
            total=len(all_icons),
        )

        downloaded_count, failed_count = download_icons_parallel(
            all_icons,
            filename_map,
            int(size),
            progress,
            task,
            max_workers=workers,
        )

    # Summary
    console.print()
    summary_table = Table(title="Download Summary", show_header=True, header_style="bold")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green")

    summary_table.add_row("Total icons found", str(len(all_icons)))
    summary_table.add_row("Successfully downloaded", str(downloaded_count))
    if failed_count > 0:
        summary_table.add_row(
            "Failed",
            str(failed_count),
            style="red",
        )

    console.print(summary_table)
    console.print(f"\n[green]✓[/green] Download complete! Files saved to: [cyan]{target_directory}[/cyan]")

    logger.info(
        "Download completed: %d succeeded, %d failed",
        downloaded_count,
        failed_count,
    )


def main() -> None:
    """Main entry point for CLI."""
    download()

