"""
DevFolio Backend - Main Server
FastAPI application serving portfolio data, cached screenshots, and the frontend.
"""

import os
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from backend.fetch_data import get_portfolio_data
import io
import os

try:
    from backend.mongo_client import get_db
    from motor.motor_asyncio import AsyncIOMotorGridFSBucket
    USE_MONGO = bool(os.getenv("MONGO_URI"))
except ImportError:
    USE_MONGO = False

# Resolve paths relative to this file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "screenshots")
FRONTEND_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "frontend")

app = FastAPI(title="DevFolio API", description="Serves developer portfolio data for the DevFolio gallery.")

# Allow the frontend (any origin for now) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keep the static mount as a fallback if Mongo isn't used
app.mount("/screenshots", StaticFiles(directory=SCREENSHOTS_DIR), name="screenshots")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="frontend_static")

def _safe_filename(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '_', name).lower()

@app.get("/api/portfolios")
async def read_portfolios():
    data = get_portfolio_data()
    
    mongo_files = set()
    if USE_MONGO:
        db = get_db()
        fs = AsyncIOMotorGridFSBucket(db)
        cursor = fs.find({})
        async for grid_out in cursor:
            mongo_files.add(grid_out.filename)

    enriched = []
    for item in data:
        safe_name = _safe_filename(item["name"])
        target_filename = f"{safe_name}_part1.jpg"
        
        if USE_MONGO:
            has_screenshots = target_filename in mongo_files
        else:
            has_screenshots = os.path.exists(os.path.join(SCREENSHOTS_DIR, target_filename))

        enriched.append({
            **item,
            "safe_name": safe_name,
            "has_screenshots": has_screenshots,
        })

    return {"count": len(enriched), "portfolios": enriched}

@app.get("/api/screenshots/{filename}")
async def get_screenshot(filename: str):
    if not USE_MONGO:
        raise HTTPException(status_code=404, detail="MongoDB not configured")
        
    db = get_db()
    fs = AsyncIOMotorGridFSBucket(db)
    
    try:
        grid_out = await fs.open_download_stream_by_name(filename)
        data = await grid_out.read()
        return StreamingResponse(io.BytesIO(data), media_type="image/png")
    except Exception:
        raise HTTPException(status_code=404, detail="Screenshot not found in MongoDB")


@app.get("/")
def serve_frontend():
    """Serves the frontend index.html at the root URL."""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
