# `backend/screenshot_service.py`

## Purpose
A Playwright-powered background job designed to capture massive amounts of developer portfolios cleanly.

## Recent Updates
1. **MongoDB GridFS Integration**: Integrated `upload_file_to_mongo` into the capturing loop. Now, as the scraper saves local `.png` files, it checks for `MONGO_URI` in the environment variables and uploads the screenshots directly to MongoDB using Motor's AsyncIOMotorGridFSBucket.
2. **5-Part Incremental Capture**: Still captures 5 sequential screenshots of each portfolio page to create a comprehensive overview of the site that the frontend strings together for its hover animation.
3. **Enterprise Playwright Features**: Uses DOM stability checkers, heavy media interception, and global CSS injection to force page animations to complete instantly, allowing rapid rendering.
