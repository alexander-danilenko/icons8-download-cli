"""Data models for Icons8 API responses."""

from pydantic import BaseModel


class Icon(BaseModel):
    """Individual icon model from Icons8 API."""

    id: str
    name: str


class IconResponse(BaseModel):
    """API response model containing list of icons."""

    success: bool
    icons: list[Icon]

