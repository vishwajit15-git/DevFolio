# screenshot_service.py — Playwright Screenshot Automation

## File Path
`backend/screenshot_service.py`

## Purpose
Uses Playwright to launch a headless Chromium browser, navigate to each developer portfolio URL, and capture incremental screenshots. Because the repository contains 1,806 uniquely built portfolios—many featuring continuous background videos, active WebSockets, or infinite data polling—relying on standard `networkidle` states is insufficient.

To create a universal capture system, this script implements:
1.  **Request Blocking (Network Routing):** Automatically intercepts and aborts any requests for `media` (videos/audio) or `websocket` connections. This prevents infinite loading loops in the background.
2.  **DOM Stability Verification:** Instead of watching network traffic, it injects a JavaScript `MutationObserver`. It monitors the HTML structure and waits until the DOM has completely stopped changing for 2.5 seconds. This guarantees all entry animations, spinners, and loading screens have physically settled.

After stability is reached, it takes 5 incremental screenshots per website, pausing briefly between scrolls. Screenshots are cached locally in `backend/screenshots/`.

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

### `wait_for_dom_stability(page, timeout_ms=30000, idle_time_ms=2500)`
Injects a `MutationObserver` script into the browser context. The script resets a timer every time the DOM mutates. It resolves the Promise (unblocking the Python script) only when the DOM has remained unchanged for `idle_time_ms` (2.5 seconds).

### `capture_universal_screenshots(url: str, developer_name: str, num_shots: int = 5) -> list[str]`
Launches a headless Chromium browser, aborts media/websocket requests, navigates to the portfolio URL, waits for DOM stability, and takes incremental screenshots by scrolling down.
- **url:** The portfolio URL to capture.
- **developer_name:** Used to generate the filename.
- **num_shots:** Number of incremental screenshots to take (default 5).
Returns a list of filepaths of the saved screenshots.

### `run_batch_job(limit: int = 3)`
Fetches portfolio data and captures universal screenshots in batch for testing. Limit is set to 3 to avoid long execution times during testing.

## Line-by-Line Explanation

```python
# Lines 1-6: Module docstring
"""
DevFolio Backend - Screenshot Service
Uses Playwright to generate and cache incremental screenshots of developer portfolios.
Implements Universal Capture strategies (DOM Stability, Request Blocking) for maximum reliability.
Runs as a standalone batch job or can be imported by the FastAPI server.
"""
```
- **Lines 1–6:** Module-level docstring reflecting the new Universal Capture logic.

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
# Lines 29-55: DOM Stability Injector
async def wait_for_dom_stability(page, timeout_ms=30000, idle_time_ms=2500):
    """..."""
    await page.evaluate("""
        (idle_time_ms) => {
            return new Promise((resolve) => {
                let timeout;
                const observer = new MutationObserver(() => {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => {
                        observer.disconnect();
                        resolve();
                    }, idle_time_ms);
                });
                observer.observe(document.body, { childList: true, subtree: true, attributes: true });
                // Initial timer in case the page is already static
                timeout = setTimeout(() => {
                    observer.disconnect();
                    resolve();
                }, idle_time_ms);
            });
        }
    """, idle_time_ms)
```
- **Lines 29-55:** This is the core of the DOM Stability method. It executes raw JavaScript in the browser. It creates a `MutationObserver` that watches `document.body`. Any time an element is added, removed, or changed, it clears and restarts the 2.5-second timer. The python script will wait at this line until the timer successfully runs out.

```python
# Lines 58-70: Main Capture Function Setup & Caching
async def capture_universal_screenshots(url: str, developer_name: str, num_shots: int = 5) -> list[str]:
    ...
```
- Skips capturing if all 5 parts are already present on disk.

```python
# Lines 72-76: Playwright Initialization
    saved_paths = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
```
- Initializes the headless browser with a strict 1080p resolution.

```python
# Lines 78-88: Network Routing & Navigation
        try:
            print(f"Visiting {developer_name}'s portfolio...")
            
            # 1. Block heavy media that causes infinite loading loops
            await page.route("**/*", lambda route: route.abort() 
                if route.request.resource_type in ["media", "websocket"] 
                else route.continue_())

            # 2. Standard load (don't wait for network idle)
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
```
- **Lines 82-85:** Sets up a request interceptor. If a website tries to load a `media` file (like a background video) or open a `websocket`, Playwright instantly aborts it. This prevents the browser from getting stuck loading heavy, continuous assets.
- **Line 88:** Navigates to the URL. Uses `wait_until="domcontentloaded"`, which only waits for the raw HTML to arrive, rather than waiting for the entire network to idle.

```python
# Lines 90-93: Triggering DOM Stability
            # 3. Wait for the page's HTML to physically stop changing
            print("  -> Waiting for animations and loading screens to settle (DOM Stability)...")
            await wait_for_dom_stability(page)
```
- **Line 93:** Calls the custom JS injector and waits for the page to visually settle.

```python
# Lines 95-104: Incremental Capture Loop
            for i in range(1, num_shots + 1):
                filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_part{i}.png")
                
                # CAPTURE: Take a screenshot of just the current visible window (not full page)
                await page.screenshot(path=filepath, full_page=False)
                print(f"  -> Saved: {filepath}")
                saved_paths.append(filepath)
                
                # SCROLL: Scroll down by exactly one viewport height
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                # A smaller wait between scroll shots for standard scroll animations
                await page.wait_for_timeout(1000) 
```
- **Line 99:** Captures the current visible area.
- **Line 103:** Scrolls down by `window.innerHeight`.
- **Line 105:** A 1-second wait to allow scroll-triggered animations to play.

```python
# Lines 107-113: Error Handling & Cleanup
            return saved_paths
        except Exception as e:
            print(f"  -> Failed ({developer_name}): {e}")
            return saved_paths
        finally:
            await browser.close()
```
- Catches errors and ensures browser shutdown.

```python
# Lines 116-144: Batch Job Runner
async def run_batch_job(limit: int = 3):
    ...
```
- Test runner logic for processing the first 3 portfolios.

```python
# Lines 147-148: Entry point
if __name__ == "__main__":
    asyncio.run(run_batch_job(limit=3))
```
- Standard Python run block.

---
*Last Updated: 2026-07-02 (Day 3 — Implemented Universal Capture with DOM Stability and Media Routing)*
