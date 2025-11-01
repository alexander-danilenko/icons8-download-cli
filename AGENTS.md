# Project: icons8-download-cli | Tech: Python 3.14+ CLI | AI Agent Rules

## BUILD & TEST
- Build: `uv build`
- Install: `uv tool install git+https://github.com/alexander-danilenko/icons8-download-cli` or `uv pip install -e .`
- Run: `icons8-download --style <style>`
- No tests currently configured

## CODE STYLE
- **Type hints**: Required for all functions/methods
- **Docstrings**: Google style for public functions
- **Naming**: `snake_case` for variables/functions, `PascalCase` for classes
- **Imports**: stdlib → third-party → local (grouped)
- **Error handling**: Specific exception types, return early pattern
- **PEP 8**: Follow style guide

## PACKAGE MANAGEMENT
- **CRITICAL**: Use `uv` only - no pip/poetry/pipenv
- **CRITICAL**: Never add packages without explicit permission
- **CRITICAL**: Ask before adding any external dependencies
- Structure: `pyproject.toml` with `hatchling` build backend
- Lock file: `uv.lock` must be committed

## PATTERNS
- **SOLID**: Follow SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion)
- **CLI**: Use `click` for all CLI commands (`@click.command`, `@click.option`, `@click.argument`)
- **Models**: Use `pydantic.BaseModel` for data validation
- **Paths**: Prefer `pathlib.Path` over `os.path`
- **I/O**: Use context managers (`with` statements)
- **Lazy imports**: Use lazy imports for heavy dependencies (e.g., `rich` components)
- **Architecture**: Separate concerns (api.py, downloader.py, models.py, cache.py)

## PROJECT SPECIFICS
- **Python version**: 3.14+ required
- **CLI entry**: `icons8_download_cli.cli:main`
- **Dependencies**: click, requests, pydantic, rich
- **Cache**: JSON-based response caching in `cache.py`
- **Downloads**: Auto-detects system Downloads folder (Windows/Linux/macOS)

## GIT
- **Commit format**: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- **Structure**: `<type>[optional scope]: <description>`
- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`
- **Breaking changes**: Use `!` after type/scope or `BREAKING CHANGE:` footer
- **Examples**: `feat: add new download option`, `fix(cli): correct error handling`
