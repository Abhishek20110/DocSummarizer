import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/doc_summarizer")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database()

folders_collection = db.get_collection("folders")

async def save_folder_results(folder_id: str, folder_name: str, results: list):
    """Saves or updates the results for a specific folder."""
    await folders_collection.update_one(
        {"folder_id": folder_id},
        {
            "$set": {
                "folder_name": folder_name,
                "results": results,
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )

async def get_folder_results(folder_id: str):
    """Retrieves results for a specific folder."""
    return await folders_collection.find_one({"folder_id": folder_id}, {"_id": 0})

async def list_processed_folders():
    """Lists all processed folders, sorted by most recent."""
    cursor = folders_collection.find({}, {"_id": 0, "folder_id": 1, "folder_name": 1, "updated_at": 1}).sort("updated_at", -1)
    return await cursor.to_list(length=100)

async def delete_folder(folder_id: str):
    """Deletes a folder from the database."""
    await folders_collection.delete_one({"folder_id": folder_id})
