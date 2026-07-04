import os
import io
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "devfolio")

# Maintain a global client to avoid reconnecting overhead
client = None

def get_db():
    global client
    if not MONGO_URI:
        raise ValueError("MONGO_URI is not set in environment.")
    if client is None:
        client = AsyncIOMotorClient(MONGO_URI)
    return client[MONGO_DB_NAME]

async def upload_file_to_mongo(local_file_path: str, filename: str) -> str:
    """
    Reads a local file and stores it in MongoDB GridFS.
    Returns the URL path that FastAPI can serve it from.
    """
    db = get_db()
    fs = AsyncIOMotorGridFSBucket(db)
    
    # Read binary
    with open(local_file_path, "rb") as f:
        file_data = f.read()

    # If file with this filename already exists, delete it so we overwrite
    cursor = fs.find({"filename": filename})
    async for grid_out in cursor:
        await fs.delete(grid_out._id)
        
    await fs.upload_from_stream(
        filename,
        io.BytesIO(file_data),
        metadata={"contentType": "image/jpeg"}
    )
    
    return f"/api/screenshots/{filename}"
