# screenshot_service.py — Playwright Screenshot Automation

## File Path
`backend/screenshot_service.py`

## Purpose
Uses Playwright to launch a headless Chromium browser, navigate to each developer portfolio URL, and capture incremental screenshots. Instead of taking a single full-page screenshot (which often misses scroll-triggered animations), the script takes 5 incremental screenshots per website. It pauses for 2.5 seconds to let CSS/JS animations finish loading, takes a screenshot of the visible window, and then scrolls down by exactly one viewport height. Screenshots are cached locally in `backend/screenshots/`.

## Dependencies
- `playwright` — Browser automation library (Python binding) for headless screenshot capture
- `os` / `pathlib` (stdlib) — File path management for the screenshots cache directory
- `asyncio` (stdlib) — Playwright's async API requires an event loop
- `re` (stdlib) — Regular expressions to sanitize developer names into safe filenames

## Connection to Other Files
- **Receives data from** `fetch_data.py` → gets the list of portfolio URLs to screenshot
- **Called by** `main.py` → server triggers screenshot generation and serves cached images (future step)
- **Output consumed by** `frontend/app.js` → frontend displays the incremental screenshots (future step)

## Functions / Classes

### `_safe_filename(name: str) -> str`
Converts a developer name into a filesystem-safe filename by replacing any non-alphanumeric character with an underscore and lowercasing.

### `capture_incremental_screenshots(url: str, developer_name: str, num_shots: int = 5) -> list[str]`
Launches a headless Chromium browser, navigates to the portfolio URL, and takes incremental screenshots by scrolling down to allow animations to load.
- **url:** The portfolio URL to capture.
- **developer_name:** Used to generate the filename.
- **num_shots:** Number of incremental screenshots to take (default 5).
Returns a list of filepaths of the saved screenshots.

### `run_batch_job(limit: int = 3)`
Fetches portfolio data and captures incremental screenshots in batch for testing. Limit is set to 3 to avoid long execution times during testing.

## Line-by-Line Explanation

```python
# Lines 1-5: Module docstring
"""
DevFolio Backend - Screenshot Service
Uses Playwright to generate and cache incremental screenshots of developer portfolios.
Runs as a standalone batch job or can be imported by the FastAPI server.
"""
```
- **Lines 1–5:** Module-level docstring explaining this file handles incremental screenshot generation and caching.

```python
# Lines 7-10: Imports
import asyncio
import os
import re
from playwright.async_api import async_playwright
```
- **Line 7:** `asyncio` for running asynchronous Python code.
- **Line 8:** `os` for filesystem path manipulation.
- **Line 9:** `re` for sanitizing filenames using regex.
- **Line 10:** `async_playwright` to launch and control the headless browser.

```python
# Lines 12-17: Directory Setup
# Resolve the screenshots directory relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "screenshots")

# Ensure the screenshots folder exists
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
```
- **Lines 12-14:** Dynamically determines the absolute path to the `screenshots/` directory so the script works no matter where it is run from.
- **Line 17:** Creates the directory if it doesn't already exist.

```python
# Lines 20-25: Filename Sanitizer
def _safe_filename(name: str) -> str:
    """..."""
    return re.sub(r'[^a-zA-Z0-9]', '_', name).lower()
```
- **Lines 20-25:** Helper function that takes a string like "John Doe" and returns "john_doe" to ensure the filename doesn't cause OS errors.

```python
# Lines 28-39: Main Capture Function Setup
async def capture_incremental_screenshots(url: str, developer_name: str, num_shots: int = 5) -> list[str]:
    """..."""
```
- **Line 28:** Main async function to capture the 5 screenshots.

```python
# Lines 40-50: Cache Checking
    safe_name = _safe_filename(developer_name)
    
    # Check if all screenshots are already cached
    cached_paths = []
    for i in range(1, num_shots + 1):
        filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_part{i}.png")
        if os.path.exists(filepath):
            cached_paths.append(filepath)
            
    if len(cached_paths) == num_shots:
        print(f"Cache hit for {developer_name}: {num_shots} parts.")
        return cached_paths
```
- **Line 40:** Sanitizes the name.
- **Lines 43-47:** Checks if all expected parts (1 through 5) already exist in the `screenshots/` directory.
- **Lines 49-51:** If all parts are cached, skip capturing and return immediately.

```python
# Lines 52-56: Playwright Initialization
    saved_paths = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
```
- **Line 52:** List to hold newly saved paths.
- **Line 54:** Initializes the Playwright async context.
- **Line 55:** Launches the Chromium browser in headless mode.
- **Line 56:** Creates a new page with a fixed `1920x1080` viewport, crucial for calculating consistent scrolls.

```python
# Lines 58-61: Navigation
        try:
            print(f"Visiting {developer_name}'s portfolio...")
            # 20-second timeout so one slow site doesn't freeze the whole batch
            await page.goto(url, timeout=20000, wait_until="load")
```
- **Line 61:** Navigates to the URL with a 20-second timeout. `wait_until="load"` ensures basic assets have loaded.

```python
# Lines 63-75: Incremental Capture Loop
            for i in range(1, num_shots + 1):
                filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_part{i}.png")
                
                # 1. WAIT: Pause for 2.5 seconds to let CSS/JS animations finish loading
                await page.wait_for_timeout(2500) 
                
                # 2. CAPTURE: Take a screenshot of just the current visible window (not full page)
                await page.screenshot(path=filepath, full_page=False)
                print(f"  -> Saved: {filepath}")
                saved_paths.append(filepath)
                
                # 3. SCROLL: Scroll down by exactly one viewport height
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
```
- **Line 63:** Loops 5 times.
- **Line 67:** Waits 2.5 seconds to allow fade-ins or slide-ups to finish.
- **Line 70:** Captures ONLY the visible viewport (full_page=False).
- **Line 74:** Executes a JavaScript command in the browser to scroll down exactly one screen height (`window.innerHeight`).

```python
# Lines 77-83: Cleanup
            return saved_paths
        except Exception as e:
            print(f"  -> Failed ({developer_name}): {e}")
            return saved_paths
        finally:
            await browser.close()
```
- **Line 80:** Catches timeout or network errors.
- **Line 83:** Ensures the browser process is closed, even if an error occurs.

```python
# Lines 86-114: Batch Processing Loop
async def run_batch_job(limit: int = 3):
    ...
```
- **Line 86:** Defines the batch runner.
- **Lines 94-97:** Safely imports `get_portfolio_data`.
- **Line 100:** Fetches the data.
- **Line 103:** Slices the list to just the `limit` (first 3).
- **Lines 106-116:** Iterates over the batch, calling `capture_incremental_screenshots`, and tracks success/failure.

```python
# Lines 120-121: Execution Entry Point
if __name__ == "__main__":
    asyncio.run(run_batch_job(limit=3))
```
- **Lines 120-121:** Runs the batch script locally with an `asyncio` event loop.

---
*Last Updated: 2026-07-02 (Day 3 — Implemented incremental screenshot capturing and scrolling)*
