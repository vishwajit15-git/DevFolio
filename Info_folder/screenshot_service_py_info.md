# screenshot_service.py — Playwright Screenshot Automation

## File Path
`backend/screenshot_service.py`

## Purpose
Uses Playwright to launch a headless Chromium browser, navigate to each developer portfolio URL, and capture incremental screenshots. To handle diverse loading screens across 1,806 portfolios, the script uses two key bypass methods:
1.  **`networkidle` Wait State:** Pauses the capture until all network requests have finished (meaning heavy assets are downloaded).
2.  **JavaScript Inject:** Searches for and hides DOM elements that look like loading screens (`[class*="load"]`, etc.) before capturing.

After ensuring the page is visible, it takes 5 incremental screenshots per website, pausing for 1.5 seconds between scrolls to allow scroll-triggered animations to load. Screenshots are cached locally in `backend/screenshots/`.

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
Launches a headless Chromium browser, navigates to the portfolio URL, bypasses loaders, and takes incremental screenshots by scrolling down.
- **url:** The portfolio URL to capture.
- **developer_name:** Used to generate the filename.
- **num_shots:** Number of incremental screenshots to take (default 5).
Returns a list of filepaths of the saved screenshots.

### `run_batch_job(limit: int = 3)`
Fetches portfolio data and captures incremental screenshots in batch for testing. Limit is set to 3 to avoid long execution times during testing.

## Line-by-Line Explanation

```python
# Lines 1-6: Module docstring
"""
DevFolio Backend - Screenshot Service
Uses Playwright to generate and cache incremental screenshots of developer portfolios.
Includes network monitoring and JS injection to bypass loading screens.
Runs as a standalone batch job or can be imported by the FastAPI server.
"""
```
- **Lines 1–6:** Module-level docstring reflecting the new loading screen bypass logic.

```python
# Lines 8-11: Imports
import asyncio
import os
import re
from playwright.async_api import async_playwright
```
- Standard imports.

```python
# Lines 13-18: Directory Setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
```
- Ensures the cache directory exists and uses absolute paths.

```python
# Lines 21-26: Filename Sanitizer
def _safe_filename(name: str) -> str:
    """..."""
    return re.sub(r'[^a-zA-Z0-9]', '_', name).lower()
```
- Sanitizes the developer name.

```python
# Lines 29-41: Main Capture Function Setup
async def capture_incremental_screenshots(url: str, developer_name: str, num_shots: int = 5) -> list[str]:
    """..."""
```
- The main capture function.

```python
# Lines 42-52: Cache Checking
    safe_name = _safe_filename(developer_name)
    cached_paths = []
    for i in range(1, num_shots + 1):
        filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_part{i}.png")
        if os.path.exists(filepath):
            cached_paths.append(filepath)
            
    if len(cached_paths) == num_shots:
        print(f"Cache hit for {developer_name}: {num_shots} parts.")
        return cached_paths
```
- Skips capturing if all 5 parts are already present on disk.

```python
# Lines 54-58: Playwright Initialization
    saved_paths = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
```
- Initializes the headless browser with a strict 1080p resolution.

```python
# Lines 60-65: NetworkIdle Navigation
        try:
            print(f"Visiting {developer_name}'s portfolio...")
            # UPGRADE 1: Wait for 'networkidle' instead of just 'load'
            # We give it a generous 30-second timeout for heavy 3D portfolios
            await page.goto(url, wait_until="networkidle", timeout=30000) 
```
- **Line 65:** The first major upgrade. `wait_until="networkidle"` pauses execution until there are 0 network connections for at least 500ms, ensuring heavy assets (like WebGL scenes) are downloaded before capturing.

```python
# Lines 67-74: JavaScript Loader Bypass
            # UPGRADE 2: Force-hide common loading screen overlays using JavaScript
            await page.evaluate("""
                const loaders = document.querySelectorAll('[class*="load"], [id*="load"], [class*="preloader"]');
                loaders.forEach(loader => loader.style.display = 'none');
            """)

            # Wait an additional 2 seconds just in case the removal triggered a fade-in animation
            await page.wait_for_timeout(2000) 
```
- **Lines 68-71:** Injects JS into the browser context. It queries for DOM elements whose class or ID contain "load" or "preloader", and sets their display to `none`. This blasts away sticky full-screen loaders that get stuck.
- **Line 74:** A hard 2-second pause lets any reveal animations finish playing after the loader disappears.

```python
# Lines 76-86: Incremental Capture Loop
            for i in range(1, num_shots + 1):
                filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_part{i}.png")
                
                # CAPTURE: Take a screenshot of just the current visible window (not full page)
                await page.screenshot(path=filepath, full_page=False)
                print(f"  -> Saved: {filepath}")
                saved_paths.append(filepath)
                
                # SCROLL: Scroll down by exactly one viewport height
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                # A smaller wait between scroll shots for standard scroll animations
                await page.wait_for_timeout(1500) 
```
- **Line 81:** Captures the current visible area.
- **Line 85:** Scrolls down by `window.innerHeight`.
- **Line 87:** A 1.5-second wait to allow scroll-triggered animations to play.

```python
# Lines 88-94: Error Handling & Cleanup
            return saved_paths
        except Exception as e:
            print(f"  -> Failed ({developer_name}). Timeout or bot block: {e}")
            return saved_paths
        finally:
            await browser.close()
```
- Catches errors and ensures browser shutdown.

```python
# Lines 97-125: Batch Job Runner
async def run_batch_job(limit: int = 3):
    ...
```
- Test runner logic for processing the first 3 portfolios.

```python
# Lines 128-129: Entry point
if __name__ == "__main__":
    asyncio.run(run_batch_job(limit=3))
```
- Standard Python run block.

---
*Last Updated: 2026-07-02 (Day 3 — Implemented loading screen bypass and networkidle)*
