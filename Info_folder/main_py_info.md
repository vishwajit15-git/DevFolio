# main.py — Backend Server Entry Point

## File Path
`backend/main.py`

## Purpose
The main FastAPI application server. It will serve portfolio data (from `feed.json`) and cached screenshots as API endpoints to the frontend.

## Dependencies
- `fastapi` — Web framework for building the REST API
- `uvicorn` — ASGI server to run the FastAPI app
- Imports from `fetch_data.py` and `screenshot_service.py`

## Connection to Other Files
- **Imports from** `fetch_data.py` → uses parsed portfolio data
- **Imports from** `screenshot_service.py` → triggers/serves cached screenshots
- **Consumed by** `frontend/app.js` → frontend fetches data from endpoints defined here

## Functions / Classes
*(Currently a placeholder — will be updated as code is written)*

## Line-by-Line Explanation

```python
# Line 1-4: Module docstring
"""
DevFolio Backend - Main Server
FastAPI application serving portfolio data and cached screenshots to the frontend.
"""
```
- **Lines 1–4:** A triple-quoted docstring that describes the module's role. This is a Python convention for documenting the purpose of a file at the top level.

---
*Last Updated: 2026-07-01 (Day 1 — Initial scaffold)*
