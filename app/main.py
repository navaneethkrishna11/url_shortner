"""
FastAPI URL Shortener Application
A modern, clean URL shortener with web interface
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import URLCreate, URLResponse
from .utils import (
    generate_short_code,
    is_valid_url,
    is_valid_custom_code,
    load_data,
    save_data,
    get_html_content
)
from .config import settings

# Initialize FastAPI app
app = FastAPI(
    title="URL Shortener",
    description="Modern URL shortener with clean UI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage
url_storage = {}
stats_storage = {}

@app.on_event("startup")
async def startup_event():
    """Load data on startup"""
    global url_storage, stats_storage
    url_storage, stats_storage = load_data()

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main HTML page"""
    return HTMLResponse(content=get_html_content())

@app.post("/shorten", response_model=URLResponse)
async def shorten_url(request: URLCreate, req: Request):
    """Create a shortened URL"""
    
    # Validate URL
    if not is_valid_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    # Handle custom code
    if request.custom_code:
        if not is_valid_custom_code(request.custom_code):
            raise HTTPException(
                status_code=400, 
                detail="Invalid custom code format"
            )
        if request.custom_code in url_storage:
            raise HTTPException(status_code=400, detail="Custom code already exists")
        short_code = request.custom_code
    else:
        short_code = generate_short_code()
    
    # Store URL mapping
    url_storage[short_code] = request.url
    stats_storage[short_code] = 0
    save_data(url_storage, stats_storage)
    
    # Build short URL
    base_url = str(req.base_url).rstrip('/')
    short_url = f"{base_url}/{short_code}"
    
    return URLResponse(
        short_url=short_url,
        original_url=request.url,
        short_code=short_code
    )

@app.get("/stats")
async def get_stats():
    """Get usage statistics"""
    total_urls = len(url_storage)
    total_clicks = sum(stats_storage.values())
    
    return {
        "total_urls": total_urls,
        "total_clicks": total_clicks
    }

@app.get("/{short_code}")
async def redirect_url(short_code: str):
    """Redirect to original URL"""
    if short_code not in url_storage:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    # Increment click count
    stats_storage[short_code] = stats_storage.get(short_code, 0) + 1
    save_data(url_storage, stats_storage)
    
    original_url = url_storage[short_code]
    return RedirectResponse(url=original_url, status_code=302)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "total_urls": len(url_storage)}