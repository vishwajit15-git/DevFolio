"""
DevFolio Backend - Screenshot Service
Uses Playwright to generate and cache incremental screenshots of developer portfolios.
Includes network monitoring and JS injection to bypass loading screens.
Runs as a standalone batch job or can be imported by the FastAPI server.
"""

import asyncio
import os
import re
from playwright.async_api import async_playwright

# Resolve the screenshots directory relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "screenshots")

# Ensure the screenshots folder exists
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def _safe_filename(name: str) -> str:
    """
    Converts a developer name into a filesystem-safe filename.
    Replaces any non-alphanumeric character with an underscore and lowercases.
    """
    return re.sub(r'[^a-zA-Z0-9]', '_', name).lower()


async def capture_incremental_screenshots(url: str, developer_name: str, num_shots: int = 5) -> list[str]:
    """
    Launches a headless Chromium browser, navigates to the portfolio URL,
    bypasses loaders, and takes incremental screenshots by scrolling down.

    Args:
        url: The portfolio URL to capture.
        developer_name: Used to generate the filename.
        num_shots: Number of incremental screenshots to take.

    Returns:
        A list of filepaths of the saved screenshots.
    """
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
        
    saved_paths = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            print(f"Visiting {developer_name}'s portfolio...")
            # UPGRADE 1: Wait for 'networkidle' instead of just 'load'
            # We give it a generous 30-second timeout for heavy 3D portfolios
            await page.goto(url, wait_until="networkidle", timeout=30000) 
            
            # UPGRADE 2: Force-hide common loading screen overlays using JavaScript
            # This looks for elements with 'loader', 'loading', or 'preloader' in their class/id and removes them.
            await page.evaluate("""
                const loaders = document.querySelectorAll('[class*="load"], [id*="load"], [class*="preloader"]');
                loaders.forEach(loader => loader.style.display = 'none');
            """)

            # Wait an additional 2 seconds just in case the removal triggered a fade-in animation
            await page.wait_for_timeout(2000) 
            
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
                
            return saved_paths
        except Exception as e:
            print(f"  -> Failed ({developer_name}). Timeout or bot block: {e}")
            return saved_paths
        finally:
            await browser.close()


async def run_batch_job(limit: int = 3):
    """
    Fetches portfolio data and captures incremental screenshots in batch.

    Args:
        limit: Number of portfolios to process (default 3 for testing).
    """
    # Import here to support both standalone and package execution
    try:
        from backend.fetch_data import get_portfolio_data
    except ImportError:
        from fetch_data import get_portfolio_data

    print("Fetching portfolio data from GitHub...")
    portfolios = get_portfolio_data()
    print(f"Found {len(portfolios)} portfolios. Processing first {limit}...\n")

    batch = portfolios[:limit]
    results = {"success": 0, "failed": 0, "cached": 0}

    for i, item in enumerate(batch, 1):
        print(f"[{i}/{len(batch)}] {item['name']}")
        filepaths = await capture_incremental_screenshots(item["url"], item["name"], num_shots=5)

        if len(filepaths) == 5:
            results["success"] += 1
        elif len(filepaths) > 0:
            results["success"] += 1 # partial success
        else:
            results["failed"] += 1

    print(f"\n--- Batch Complete ---")
    print(f"Success/Cached/Partial: {results['success']} | Failed: {results['failed']}")


if __name__ == "__main__":
    asyncio.run(run_batch_job(limit=3))
