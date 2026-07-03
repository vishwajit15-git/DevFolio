# `requirements.txt`

## Dependencies
- `fastapi`: Core asynchronous API backend framework.
- `uvicorn`: ASGI server to run the FastAPI app.
- `playwright`: The core scraping engine used to capture the DOM structure and screenshots.
- `beautifulsoup4`: For initial DOM parsing of the master README.md markdown table.
- `requests`: Used for retrieving the raw developer portfolio list from GitHub.
- `boto3`: AWS SDK used to connect to the S3-compatible Cloudflare R2 Storage API.
- `python-dotenv`: Used for securely loading environment variables for R2 credentials.
