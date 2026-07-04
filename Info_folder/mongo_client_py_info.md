# `backend/mongo_client.py`

## Purpose
A MongoDB asynchronous client module created to interact with the MongoDB Atlas API for DevFolio image hosting.

## Features
1. Uses `motor` and `pymongo` to interface asynchronously with MongoDB.
2. Authenticates securely using `.env` secrets (`MONGO_URI`, `MONGO_DB_NAME`).
3. Uses MongoDB **GridFS** (via `AsyncIOMotorGridFSBucket`) to bypass MongoDB's 16MB document limit and effectively store thousands of screenshot image files directly in the database.
4. Returns an API path `/api/screenshots/...` that the FastAPI server routes to stream the images directly out of MongoDB to the frontend.
