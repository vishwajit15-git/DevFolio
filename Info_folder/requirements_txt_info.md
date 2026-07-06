# `requirements.txt`

## Dependencies
- `fastapi`: Core asynchronous API backend framework.
- `uvicorn`: ASGI server to run the FastAPI app.
- `playwright`: The core scraping engine used to capture the DOM structure and screenshots.
- `requests`: Used for retrieving the raw developer portfolio list (`feed.json`) from GitHub.
- `motor`: Asynchronous MongoDB driver for Python, used for GridFS image storage/retrieval.
- `pymongo`: Synchronous MongoDB driver, required by Motor as a dependency.
- `python-dotenv`: Used for securely loading environment variables (MongoDB URI, DB name).
- `aiofiles`: Async file I/O used by FastAPI for serving static files and streaming responses.
- `pillow`: Image processing library (used for screenshot format conversion if needed).
