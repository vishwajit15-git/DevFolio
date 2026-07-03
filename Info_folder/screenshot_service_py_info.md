# `backend/screenshot_service.py`

## Purpose
A Playwright-powered background job designed to capture massive amounts of developer portfolios cleanly.

## Recent Updates
1. **Cloudflare R2 Integration**: Integrated `upload_file_to_r2` into the capturing loop. Now, as the scraper saves local `.png` files, it checks for `R2_ACCOUNT_ID` in the environment variables and securely streams the screenshots directly to a Cloudflare R2 bucket.
2. **5-Part Incremental Capture**: Still captures 5 sequential screenshots of each portfolio page to create a comprehensive overview of the site that the frontend strings together for its hover animation.
3. **Enterprise Playwright Features**: Uses DOM stability checkers, heavy media interception, and global CSS injection to force page animations to complete instantly, allowing rapid rendering.
