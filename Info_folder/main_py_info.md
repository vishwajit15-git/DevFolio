# main.py — Backend Server Entry Point

## File Path
`backend/main.py`

## Purpose
The main FastAPI application server. Creates a REST API with endpoints for portfolio data and screenshot serving. Mounts the frontend as a static file directory and integrates with MongoDB Atlas GridFS for persistent image storage.

## Dependencies
- `fastapi` — Web framework for building the REST API
- `fastapi.middleware.cors.CORSMiddleware` — Handles Cross-Origin Resource Sharing headers
- `fastapi.staticfiles.StaticFiles` — Serves the frontend static files
- `fastapi.responses.StreamingResponse` — Streams screenshot images from MongoDB GridFS
- `backend.fetch_data.get_portfolio_data` — Local import for portfolio data fetching
- `backend.mongo_client` — MongoDB GridFS client for image storage/retrieval

## Connection to Other Files
- **Imports from** `fetch_data.py` → calls `get_portfolio_data()` to get parsed & filtered portfolio data
- **Imports from** `mongo_client.py` → uses GridFS bucket to serve screenshot images
- **Consumed by** `frontend/app.js` → frontend fetches from `/api/portfolios` and `/api/screenshots/`

## API Endpoints

| Method | Path | Response | Description |
|---|---|---|---|
| `GET` | `/api/portfolios` | `{ count: int, portfolios: list }` | Returns all 1,157 filtered portfolios with names, roles, URLs, and `has_screenshots` status |
| `GET` | `/api/screenshots/{filename}` | Binary image stream | Serves a screenshot image from MongoDB GridFS (or local fallback) |
| `GET` | `/` | HTML | Serves the frontend `index.html` |
| `GET` | `/static/*` | Static files | Serves CSS, JS, and asset files from the `frontend/` directory |

## Key Implementation Details

### Screenshot Serving Priority
1. First checks MongoDB GridFS for the requested filename
2. Falls back to local `screenshots/` directory if MongoDB is unavailable
3. Returns 404 if the file doesn't exist in either location

### Portfolio Data Enrichment
The `/api/portfolios` endpoint enriches each portfolio entry with:
- `safe_name` — URL-safe filename derived from the developer's name
- `has_screenshots` — Boolean indicating if screenshot files exist (checked in both MongoDB and local storage)

---
*Last Updated: 2026-07-06 (Updated endpoint docs, added screenshot serving and static file mounting)*
