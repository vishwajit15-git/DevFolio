"""
DevFolio Backend - Screenshot Service
Uses Playwright to generate and cache incremental screenshots of developer portfolios.

Enterprise Scraper Implementations:
1. Media/WebSocket Routing (Prevents infinite loading loops)
2. Global CSS Injection (Instantly kills animations, reveals scroll-locked content)
3. DOM Stability Observer (Waits for physical rendering to settle)
4. JS Loader Bypass (Force-hides stuck loader overlays)
"""

import asyncio
import os
import re
from playwright.async_api import async_playwright

# Resolve the screenshots directory relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "screenshots")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def _safe_filename(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '_', name).lower()


async def wait_for_dom_stability(page, timeout_ms=30000, idle_time_ms=2500):
    """
    Injects a script to wait until the DOM stops mutating for `idle_time_ms`,
    or forces a resolution after `timeout_ms` to prevent infinite hangs.
    """
    await page.evaluate("""
        ({idle_time_ms, timeout_ms}) => {
            return new Promise((resolve) => {
                let idleTimeout;
                let forceTimeout;
                
                const observer = new MutationObserver(() => {
                    clearTimeout(idleTimeout);
                    idleTimeout = setTimeout(() => {
                        observer.disconnect();
                        clearTimeout(forceTimeout);
                        resolve();
                    }, idle_time_ms);
                });
                
                observer.observe(document.body, { childList: true, subtree: true, attributes: true });
                
                idleTimeout = setTimeout(() => {
                    observer.disconnect();
                    clearTimeout(forceTimeout);
                    resolve();
                }, idle_time_ms);
                
                forceTimeout = setTimeout(() => {
                    observer.disconnect();
                    clearTimeout(idleTimeout);
                    resolve();
                }, timeout_ms);
            });
        }
    """, {"idle_time_ms": idle_time_ms, "timeout_ms": timeout_ms})


async def capture_universal_screenshots(url: str, developer_name: str, num_shots: int = 5) -> list[str]:
    safe_name = _safe_filename(developer_name)
    
    cached_paths = []
    for i in range(1, num_shots + 1):
        filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_part{i}.png")
        if os.path.exists(filepath):
            cached_paths.append(filepath)
            
    if len(cached_paths) == num_shots:
        print(f"Cache hit for {developer_name}: {num_shots} parts.")
        return cached_paths
        
    saved_paths = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            print(f"Visiting {developer_name}'s portfolio...")
            
            # STRATEGY 1: Media/WebSocket Routing
            # Aborts heavy media that blocks the page load event or causes infinite polling
            await page.route("**/*", lambda route: route.abort() 
                if route.request.resource_type in ["media", "websocket"] 
                else route.continue_())

            # STRATEGY 2: Global CSS Injection
            # Injected before the page loads. Kills all animations/transitions so progress bars instantly 
            # jump to 100%, and forces scroll-reveal libraries (like AOS) to make content visible immediately.
            await page.add_init_script("""
                const style = document.createElement('style');
                style.innerHTML = `
                    *, *::before, *::after {
                        transition: none !important;
                        animation: none !important;
                        animation-delay: -0.01ms !important;
                        animation-duration: 0.01ms !important;
                        animation-iteration-count: 1 !important;
                        scroll-behavior: auto !important;
                    }
                    [data-aos], .reveal, .fade-in, .hidden, .opacity-0 {
                        opacity: 1 !important;
                        transform: none !important;
                        visibility: visible !important;
                    }
                `;
                document.addEventListener('DOMContentLoaded', () => document.head.appendChild(style));
            """)

            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            
            # STRATEGY 3: JS Loader Bypass
            # Force-hide persistent loader overlays
            await page.evaluate("""
                const loaders = document.querySelectorAll('[class*="load"], [id*="load"], [class*="preloader"]');
                loaders.forEach(loader => loader.style.display = 'none');
            """)

            # STRATEGY 4: DOM Stability
            print("  -> Waiting for animations and loading screens to settle (DOM Stability)...")
            await wait_for_dom_stability(page)
            
            # Try to load MongoDB client
            mongo_upload_enabled = bool(os.getenv("MONGO_URI"))
            if mongo_upload_enabled:
                try:
                    from backend.mongo_client import upload_file_to_mongo
                except ImportError:
                    try:
                        from mongo_client import upload_file_to_mongo
                    except ImportError:
                        mongo_upload_enabled = False

            for i in range(1, num_shots + 1):
                filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_part{i}.png")
                
                await page.screenshot(path=filepath, full_page=False)
                print(f"  -> Saved: {filepath}")
                saved_paths.append(filepath)
                
                # Upload to MongoDB GridFS
                if mongo_upload_enabled:
                    try:
                        mongo_url = await upload_file_to_mongo(filepath, f"{safe_name}_part{i}.png")
                        print(f"  -> Uploaded to MongoDB GridFS: {mongo_url}")
                    except Exception as e:
                        print(f"  -> MongoDB Upload Failed: {e}")
                
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                await page.wait_for_timeout(1000) 
                
            return saved_paths
            
        except Exception as e:
            print(f"  -> Failed ({developer_name}) - Will use Fallback UI. Error: {e}")
            # If all strategies fail (e.g. strict bot blockers), we return whatever we captured (if any)
            # The frontend will be designed to handle < 5 images by showing a fallback gradient UI.
            return saved_paths
        finally:
            await browser.close()


async def run_batch_job(limit: int = 5):
    try:
        from backend.fetch_data import get_portfolio_data
    except ImportError:
        from fetch_data import get_portfolio_data

    import random
    print("Fetching portfolio data from GitHub...")
    portfolios = get_portfolio_data()
    
    batch = random.sample(portfolios, min(limit, len(portfolios)))
    print(f"Found {len(portfolios)} portfolios. Processing {limit} random ones...\n")

    results = {"success": 0, "failed": 0, "cached": 0}

    for i, item in enumerate(batch, 1):
        print(f"[{i}/{len(batch)}] {item['name']}")
        filepaths = await capture_universal_screenshots(item["url"], item["name"], num_shots=5)

        if len(filepaths) == 5:
            results["success"] += 1
        elif len(filepaths) > 0:
            results["success"] += 1 # partial success
        else:
            results["failed"] += 1

    print(f"\n--- Batch Complete ---")
    print(f"Success/Cached/Partial: {results['success']} | Failed: {results['failed']}")


if __name__ == "__main__":
    asyncio.run(run_batch_job(limit=5))
