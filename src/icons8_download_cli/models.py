"""Data models for Icons8 API responses."""

from typing import Optional

from pydantic import BaseModel, Field


class Icon(BaseModel):
    """Individual icon model from Icons8 API."""

    id: str
    name: str
    platform: str
    timestamp: int
    url: str
    common_id: str = Field(alias="commonId")
    common_name: str = Field(alias="commonName")
    category: str
    is_color: bool = Field(alias="isColor")
    need_background: bool = Field(alias="needBackground")
    suggested_background_color: Optional[str] = Field(
        alias="suggestedBackgroundColor",
        default=None,
    )
    is_animated: bool = Field(alias="isAnimated")
    free: bool
    is_external: bool = Field(alias="isExternal")
    is_original: bool = Field(alias="isOriginal")


class IconResponse(BaseModel):
    """API response model containing list of icons."""

    success: bool
    icons: list[Icon]

