"""
DevFolio Backend - Main Server
FastAPI application serving portfolio data, cached screenshots, and the frontend.
"""

import os
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.fetch_data import get_portfolio_data

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

# Mount the screenshots directory so images are accessible at /screenshots/<filename>
app.mount("/screenshots", StaticFiles(directory=SCREENSHOTS_DIR), name="screenshots")

# Mount frontend static assets (CSS, JS, images) at /static
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="frontend_static")


def _safe_filename(name: str) -> str:
    """Mirrors the screenshot_service filename logic."""
    return re.sub(r'[^a-zA-Z0-9]', '_', name).lower()


@app.get("/api/portfolios")
def read_portfolios():
    """
    Returns all developer portfolios with cleaned names, parsed roles,
    safe filenames for screenshot lookup, and a capture status flag.
    Response format: { count: int, portfolios: list[dict] }
    """
    data = get_portfolio_data()

    # Enrich each portfolio entry with screenshot availability info
    enriched = []
    for item in data:
        safe_name = _safe_filename(item["name"])
        part1_path = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_part1.png")
        has_screenshots = os.path.exists(part1_path)

        enriched.append({
            **item,
            "safe_name": safe_name,
            "has_screenshots": has_screenshots,
        })

    return {"count": len(enriched), "portfolios": enriched}


@app.get("/")
def serve_frontend():
    """Serves the frontend index.html at the root URL."""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
