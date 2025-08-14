"""
Configuration settings for URL shortener
"""

import os
from typing import List


class Settings:
    """Application settings"""
    
    # App settings
    APP_NAME: str = "URL Shortener"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://*.vercel.app"
    ]
    
    # Storage settings
    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    DATA_FILE: str = os.path.join(DATA_DIR, "url_data.json")
    STATS_FILE: str = os.path.join(DATA_DIR, "stats_data.json")
    
    # Short code settings
    SHORT_CODE_LENGTH: int = 6
    CUSTOM_CODE_MIN_LENGTH: int = 3
    CUSTOM_CODE_MAX_LENGTH: int = 20


settings = Settings()