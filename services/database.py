import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/doc_summarizer")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database()

folders_collection = db.get_collection("folders")
users_collection = db.get_collection("users")

async def create_user(username: str, password_hash: str, is_active: bool = True):
    logger.info(f"Creating new user record for: {username}")
    user = {
        "username": username,
        "password_hash": password_hash,
        "is_active": is_active,
        "created_at": datetime.utcnow()
    }
    return await users_collection.insert_one(user)

async def get_user_by_username(username: str):
    logger.debug(f"Fetching user record for: {username}")
    return await users_collection.find_one({"username": username})

async def save_folder_results(folder_id: str, folder_name: str, results: list, username: str):
    """Saves or updates the results for a specific folder."""
    logger.info(f"Saving {len(results)} results for folder {folder_name} (ID: {folder_id}) by {username}")
    await folders_collection.update_one(
        {"folder_id": folder_id, "username": username},
        {
            "$set": {
                "folder_name": folder_name,
                "results": results,
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )

async def get_folder_results(folder_id: str, username: str):
    """Retrieves results for a specific folder."""
    return await folders_collection.find_one({"folder_id": folder_id, "username": username}, {"_id": 0})

async def list_processed_folders(username: str):
    """Lists all processed folders, sorted by most recent."""
    cursor = folders_collection.find({"username": username}, {"_id": 0, "folder_id": 1, "folder_name": 1, "updated_at": 1}).sort("updated_at", -1)
    return await cursor.to_list(length=100)

async def delete_folder(folder_id: str, username: str):
    """Deletes a folder from the database."""
    logger.info(f"Deleting folder record (ID: {folder_id}) requested by {username}")
    await folders_collection.delete_one({"folder_id": folder_id, "username": username})
