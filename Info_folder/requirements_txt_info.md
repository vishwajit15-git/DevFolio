# requirements.txt — Python Dependencies

## File Path
`backend/requirements.txt`

## Purpose
Lists all Python packages required by the backend. Used with `pip install -r requirements.txt` to install dependencies into the virtual environment.

## Dependencies Listed
| Package | Role |
|---|---|
| `fastapi` | Modern async web framework for serving the REST API |
| `uvicorn[standard]` | ASGI server that runs the FastAPI app (includes websocket & HTTP/2 extras) |
| `playwright` | Browser automation for capturing full-page portfolio screenshots |
| `requests` | HTTP library for downloading `feed.json` from GitHub |

## Connection to Other Files
- **Used by** all backend Python files — defines what packages are available in the project
- **Consumed during setup** — `pip install -r backend/requirements.txt`

## Line-by-Line Explanation

```text
# Line 1: fastapi
fastapi
```
- Installs the FastAPI web framework used in `main.py`.

```text
# Line 2: uvicorn[standard]
uvicorn[standard]
```
- Installs uvicorn with extra dependencies (e.g., `uvloop`, `httptools`) for better performance. This is the server that actually runs the FastAPI app.

```text
# Line 3: playwright
playwright
```
- Installs Playwright Python bindings. After install, `playwright install chromium` must be run separately to download the browser binary.

```text
# Line 4: requests
requests
```
- Installs the `requests` HTTP library used in `fetch_data.py` to download `feed.json`.

---
*Last Updated: 2026-07-01 (Day 1 — Initial scaffold)*
