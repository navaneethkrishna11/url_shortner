"""
Pydantic models for URL shortener
"""

from pydantic import BaseModel, HttpUrl
from typing import Optional


class URLCreate(BaseModel):
    """Request model for creating short URL"""
    url: str
    custom_code: Optional[str] = None


class URLResponse(BaseModel):
    """Response model for shortened URL"""
    short_url: str
    original_url: str
    short_code: str


class StatsResponse(BaseModel):
    """Response model for statistics"""
    total_urls: int
    total_clicks: int