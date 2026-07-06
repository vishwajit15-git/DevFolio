# `backend/screenshot_service.py`

## Purpose
A Playwright-powered background job designed to capture massive amounts of developer portfolios cleanly. Runs independently from the API server as a standalone script.

## Recent Updates
1. **MongoDB GridFS Integration**: Integrated `upload_file_to_mongo` into the capturing loop. As the scraper saves local `.jpg` files, it checks for `MONGO_URI` in the environment and uploads screenshots directly to MongoDB Atlas using Motor's `AsyncIOMotorGridFSBucket`.
2. **3-Part Incremental Capture**: Captures 3 sequential screenshots of each portfolio page (top, middle, bottom) to create a comprehensive overview that the frontend stitches together for its hover-scroll animation.
3. **Windows Console Fix**: All developer names are ASCII-encoded before printing to prevent `UnicodeEncodeError` crashes on Windows terminals with CP1252 encoding.
4. **Cache Hit Detection**: Before processing a portfolio, checks for existing `.jpg` files in the local `screenshots/` directory. Skips already-captured portfolios to allow safe resumption after interruptions.
5. **Enterprise Playwright Features**: Uses DOM stability checkers, heavy media interception (aborts images/videos/websockets during load), and global CSS injection to force page animations to complete instantly, allowing rapid rendering.
6. **Excluded Names Filtering**: The scraper inherits the filtered portfolio list from `fetch_data.py`, which already excludes the 149 blacklisted developers.
7. **Error Resilience**: Catches all exceptions per-portfolio and continues scraping. Error messages are ASCII-sanitized to prevent encoding crashes.
8. **12-Second Page Timeout**: Uses a tight page-load timeout to skip unresponsive or extremely heavy portfolio sites.
