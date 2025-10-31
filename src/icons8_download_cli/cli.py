"""CLI entry point and command definitions."""

import logging
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

from icons8_download_cli.api import fetch_all_icons
from icons8_download_cli.downloader import download_icon, resolve_filenames
from icons8_download_cli.models import Icon

console = Console()

# Size choices enum
SIZE_CHOICES = click.Choice(["24", "48", "96", "192", "384", "512"], case_sensitive=False)


def get_default_downloads_dir() -> Path:
    """
    Get OS-specific Downloads directory.

    Returns:
        Path to Downloads directory
    """
    downloads_dir = Path.home() / "Downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    return downloads_dir


def setup_file_logging(target_directory: Path) -> None:
    """
    Setup file logging to target directory.

    Args:
        target_directory: Directory where log file will be created
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = target_directory / f"download-log-{timestamp}.log"

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
    type=click.Path(exists=False, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Target directory for downloaded icons (defaults to Downloads)",
)
@click.option(
    "--size",
    type=SIZE_CHOICES,
    default="512",
    help="Icon size (default: 512)",
)
@click.option(
    "--style",
    type=str,
    default=None,
    help="Icon style filter",
)
@click.option(
    "--query",
    type=str,
    default=None,
    help="Search query term (required if style is not provided)",
)
def download(
    target_directory: Path | None,
    size: str,
    style: str | None,
    query: str | None,
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
    logger.info("Parameters: size=%s, style=%s, query=%s", size, style, query)

    console.print(f"\n[bold]Icons8 Download CLI[/bold]")
    console.print(f"Target directory: [cyan]{target_directory}[/cyan]")
    console.print(f"Size: [cyan]{size}[/cyan]px")
    if style:
        console.print(f"Style: [cyan]{style}[/cyan]")
    if query:
        console.print(f"Query: [cyan]{query}[/cyan]")
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

    # Download icons with progress
    console.print("[yellow]Downloading icons...[/yellow]")
    downloaded_count = 0
    failed_count = 0

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

        for icon in all_icons:
            file_path = filename_map[icon.id]
            success = download_icon(
                icon,
                file_path,
                int(size),
                progress,
                task,
            )
            if success:
                downloaded_count += 1
            else:
                failed_count += 1

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

