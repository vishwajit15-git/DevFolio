# screenshot_service.py — Playwright Screenshot Automation

## File Path
`backend/screenshot_service.py`

## Purpose
Uses Playwright to launch a headless Chromium browser, navigate to each developer portfolio URL, and capture incremental screenshots. 

Because the repository contains 1,806 uniquely built portfolios, this script implements a **4-Layer Enterprise Universal Capture Strategy** to defeat complex loading screens, infinite background media, and scroll-locked content:
1.  **Media/WebSocket Routing:** Intercepts and aborts any requests for `media` (videos/audio) or `websocket` connections to prevent infinite loading loops.
2.  **Global CSS Injection (The Silver Bullet):** Injects a `<style>` tag into the page before it loads. It forces `transition: none` and `animation-duration: 0.01ms` globally. This makes all CSS-based progress bars instantly jump to 100%. It also overrides opacity and transforms on common scroll-reveal classes (e.g., `[data-aos]`) to ensure content is immediately visible.
3.  **JS Loader Bypass:** Force-hides any remaining DOM elements that contain "load" or "preloader" in their ID or class.
4.  **DOM Stability Verification:** Uses a `MutationObserver` to wait until the physical HTML structure stops changing for 2.5 seconds (or hits a 30s hard timeout), guaranteeing the page has settled.

After stability is reached, it takes 5 incremental screenshots per website. Screenshots are cached locally in `backend/screenshots/`.

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
Injects a `MutationObserver` script into the browser context. It resolves the Promise only when the DOM has remained unchanged for 2.5 seconds, or forcibly resolves after 30 seconds to prevent hangs from continuous animations.

### `capture_universal_screenshots(url: str, developer_name: str, num_shots: int = 5) -> list[str]`
Launches a headless Chromium browser and executes the 4-layer capture strategy to capture 5 high-quality incremental screenshots. Returns a list of filepaths.

### `run_batch_job(limit: int = 5)`
Fetches portfolio data and captures universal screenshots in batch for testing. Selects `limit` random portfolios to process.

## Line-by-Line Explanation

```python
# Lines 1-8: Module docstring
"""
DevFolio Backend - Screenshot Service
...
"""
```
- Module-level docstring reflecting the new 4-layer strategy.

```python
# Lines 10-21: Imports and Directory Setup
import asyncio
...
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "screenshots")
```
- Standard imports and absolute path setup.

```python
# Lines 27-60: DOM Stability Injector
async def wait_for_dom_stability(page, timeout_ms=30000, idle_time_ms=2500):
    ...
```
- Implements the `MutationObserver` with the hard 30-second timeout fallback.

```python
# Lines 63-82: Main Capture Function Setup & Caching
async def capture_universal_screenshots(url: str, developer_name: str, num_shots: int = 5) -> list[str]:
    ...
```
- Skips capturing if all 5 parts are already present on disk.

```python
# Lines 84-88: Playwright Initialization
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
```
- Initializes the headless browser.

```python
# Lines 93-97: Strategy 1 - Media Routing
            await page.route("**/*", lambda route: route.abort() 
                if route.request.resource_type in ["media", "websocket"] 
                else route.continue_())
```
- Kills heavy infinite background media and websocket data streams.

```python
# Lines 99-119: Strategy 2 - Global CSS Injection
            await page.add_init_script("""
                const style = document.createElement('style');
                style.innerHTML = `
                    *, *::before, *::after {
                        transition: none !important;
                        animation: none !important;
                        ...
                    }
                    [data-aos], .reveal, .fade-in, .hidden, .opacity-0 {
                        opacity: 1 !important;
                        ...
                    }
                `;
                document.addEventListener('DOMContentLoaded', () => document.head.appendChild(style));
            """)
```
- **The Silver Bullet.** This script executes before the page renders. It overrides all CSS animation timers to 0, forcing progress bars to instantly skip to 100%. It also targets common classes used by scroll-reveal libraries (like AOS) and forces them to have `opacity: 1`. This stops the scraper from capturing empty white pages.

```python
# Lines 121-127: Navigation & Strategy 3 - JS Loader Bypass
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            
            await page.evaluate("""
                const loaders = document.querySelectorAll('[class*="load"], [id*="load"], [class*="preloader"]');
                loaders.forEach(loader => loader.style.display = 'none');
            """)
```
- Navigates and forcefully hides any remaining sticky loader overlays.

```python
# Lines 129-142: Strategy 4 - DOM Stability & Incremental Capture Loop
            print("  -> Waiting for animations and loading screens to settle (DOM Stability)...")
            await wait_for_dom_stability(page)
            
            for i in range(1, num_shots + 1):
                ...
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                await page.wait_for_timeout(1000) 
```
- Waits for the physical DOM structure to stop changing, then captures the 5 scrolling sections.

```python
# Lines 144-151: Error Handling & Cleanup
        except Exception as e:
            print(f"  -> Failed ({developer_name}) - Will use Fallback UI. Error: {e}")
            return saved_paths
        finally:
            await browser.close()
```
- Robust error handling. If a site completely blocks the bot, we return what we have (or an empty list). The frontend will be instructed to show a fallback UI instead of crashing.

```python
# Lines 153-176: Batch Job Runner
async def run_batch_job(limit: int = 5):
    ...
```
- Fetches the full list of 1,806 portfolios using `get_portfolio_data()`.
- **Randomization:** Uses `random.sample(portfolios, min(limit, len(portfolios)))` to pick 5 random developers instead of always starting at the top of the list. This provides a broader test of the scraper's universal capabilities across diverse web architectures.
- Tracks `success`, `failed`, and `cached` counts and outputs a final batch summary.

---
*Last Updated: 2026-07-02 (Day 3 — Implemented Global CSS Injection)*
