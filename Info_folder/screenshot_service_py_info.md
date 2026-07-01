# screenshot_service.py — Playwright Screenshot Automation

## File Path
`backend/screenshot_service.py`

## Purpose
Uses Playwright to launch a headless Chromium browser, navigate to each developer portfolio URL, and capture a full-page screenshot. Screenshots are cached locally in `backend/screenshots/` to avoid re-capturing on every request. This is the core innovation — it bypasses `X-Frame-Options` security restrictions that prevent iframes.

## Dependencies
- `playwright` — Browser automation library (Python binding) for headless screenshot capture
- `os` / `pathlib` (stdlib) — File path management for the screenshots cache directory
- `asyncio` (stdlib) — Playwright's async API requires an event loop

## Connection to Other Files
- **Receives data from** `fetch_data.py` → gets the list of portfolio URLs to screenshot
- **Called by** `main.py` → server triggers screenshot generation and serves cached images
- **Output consumed by** `frontend/app.js` → frontend displays the screenshots in hover-to-scroll cards

## Functions / Classes
*(Currently a placeholder — will be updated as code is written)*

## Line-by-Line Explanation

```python
# Line 1-4: Module docstring
"""
DevFolio Backend - Screenshot Service
Uses Playwright to generate and cache full-page screenshots of developer portfolios.
"""
```
- **Lines 1–4:** Module-level docstring explaining this file handles the Playwright-based screenshot generation and caching logic.

---
*Last Updated: 2026-07-01 (Day 1 — Initial scaffold)*
