# `backend/mongo_client.py`

## Purpose
A MongoDB asynchronous client module for interfacing with MongoDB Atlas for DevFolio image hosting.

## Features
1. Uses `motor` (async MongoDB driver) and `pymongo` to interface asynchronously with MongoDB Atlas.
2. Authenticates securely using `.env` secrets (`MONGO_URI`, `MONGO_DB_NAME`).
3. Uses MongoDB **GridFS** (via `AsyncIOMotorGridFSBucket`) to bypass MongoDB's 16MB document limit and effectively store thousands of screenshot image files directly in the database.
4. Provides `upload_file_to_mongo()` function that handles file uploads with automatic overwrite (deletes existing files with the same filename before uploading).
5. Provides `get_db()` function that returns the Motor database instance for direct GridFS operations.
6. Returns API paths like `/api/screenshots/{filename}` that the FastAPI server routes to stream images directly out of MongoDB to the frontend.

## Connection to Other Files
- **Used by** `main.py` → serves screenshots via `/api/screenshots/{filename}` endpoint
- **Used by** `screenshot_service.py` → uploads captured screenshots to GridFS
- **Used by** `delete_portfolios.py` → deletes excluded portfolio screenshots from GridFS
