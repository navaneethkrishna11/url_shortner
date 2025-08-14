#!/usr/bin/env python3
"""
Entry point for URL Shortener application
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print(f"🚀 Starting URL Shortener on http://{settings.HOST}:{settings.PORT}")
    print(f"📁 Data directory: {settings.DATA_DIR}")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        input("Press Enter to exit.")