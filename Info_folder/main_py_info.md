# main.py — Backend Server Entry Point

## File Path
`backend/main.py`

## Purpose
The main FastAPI application server. Creates a REST API with a single endpoint (`/api/portfolios`) that calls the data fetcher and returns structured portfolio data as JSON. Includes CORS middleware so the frontend can make cross-origin requests.

## Dependencies
- `fastapi` — Web framework for building the REST API
- `fastapi.middleware.cors.CORSMiddleware` — Handles Cross-Origin Resource Sharing headers
- `backend.fetch_data.get_portfolio_data` — Local import (uses package prefix since uvicorn runs from project root)

## Connection to Other Files
- **Imports from** `fetch_data.py` → calls `get_portfolio_data()` to get parsed portfolio data
- **Will import from** `screenshot_service.py` → future endpoints for serving cached screenshots
- **Consumed by** `frontend/app.js` → frontend fetches from `/api/portfolios`

## API Endpoints

| Method | Path | Response | Description |
|---|---|---|---|
| `GET` | `/api/portfolios` | `{ count: int, portfolios: list }` | Returns all 1,806 parsed portfolios with names, roles, and URLs |

## Line-by-Line Explanation

```text
# Lines 1-4: Module docstring
"""
DevFolio Backend - Main Server
FastAPI application serving portfolio data and cached screenshots to the frontend.
"""
```
- **Lines 1–4:** Module-level docstring describing the server's role.

```text
# Lines 6-8: Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.fetch_data import get_portfolio_data
```
- **Line 6:** Imports the `FastAPI` class — the core web framework.
- **Line 7:** Imports `CORSMiddleware` to allow cross-origin requests from the frontend.
- **Line 8:** Imports `get_portfolio_data` using the `backend.` package prefix. This is required because `uvicorn backend.main:app` runs from the project root, so Python resolves imports relative to the root — not relative to `backend/`.

```text
# Line 10: App initialization
app = FastAPI(title="DevFolio API", description="Serves developer portfolio data for the DevFolio gallery.")
```
- **Line 10:** Creates the FastAPI app instance. The `title` and `description` appear in the auto-generated Swagger docs at `/docs`.

```text
# Lines 12-17: CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```
- **Line 13:** Registers CORS middleware on the app.
- **Line 14:** `allow_origins=["*"]` — permits requests from any origin (for development).
- **Line 15:** `allow_methods=["*"]` — allows all HTTP methods.
- **Line 16:** `allow_headers=["*"]` — allows all request headers.

```text
# Lines 20-28: Portfolio endpoint
@app.get("/api/portfolios")
def read_portfolios():
    """
    Returns all developer portfolios with cleaned names and parsed roles.
    Response format: { count: int, portfolios: list[dict] }
    """
    data = get_portfolio_data()
    return {"count": len(data), "portfolios": data}
```
- **Line 20:** `@app.get` decorator registers this function for `GET /api/portfolios`.
- **Line 21:** Handler function name — used in Swagger docs.
- **Lines 22–25:** Docstring describing response format.
- **Line 26:** Calls `get_portfolio_data()` to fetch and parse all 1,806 portfolios.
- **Line 27:** Returns a dict with `count` and `portfolios`. FastAPI auto-serializes to JSON.

---
*Last Updated: 2026-07-02 (Day 2 — Full implementation, fixed import path to use backend. prefix)*
