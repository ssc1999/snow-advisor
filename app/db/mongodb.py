import os
from pymongo import MongoClient, ASCENDING
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["snow_advising"]
collection = db["daily_data"]
resorts_collection = db["resorts"]
all_resorts_collection = db["all_resorts"]

# Ensure unique indexes for `resort_name` fields in collections
collection.create_index([("resort_name", ASCENDING)], unique=True)
resorts_collection.create_index([("resort_name", ASCENDING)], unique=True)
all_resorts_collection.create_index([("resort_name", ASCENDING)], unique=True)

def save_daily_data(resort_name, data):
    # Ensure no existing "date" field conflict on update
    data.pop("date", None)
    data["date"] = datetime.now().strftime("%Y-%m-%d")
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Upsert data by `resort_name`
    collection.find_one_and_replace(
        {"resort_name": resort_name},
        data,
        upsert=True
    )
    # Update resort cache
    save_resort_cache({"resort_name": resort_name, "last_updated": last_updated})
    
    return True

def get_resorts_cache():
    """Retrieve all resorts from `resorts` collection."""
    resorts = resorts_collection.find()
    return [{**resort, "_id": str(resort["_id"])} for resort in resorts]  # Convert `_id` to string

def get_all_resorts():
    """Retrieve all resorts from `all_resorts` collection."""
    resorts = all_resorts_collection.find()
    return [{**resort, "_id": str(resort["_id"])} for resort in resorts]  # Convert `_id` to string for JSON

def save_resort_cache(resort_data):
    """Save or update a resort in `resorts` cache with last_updated info."""
    resorts_collection.update_one(
        {"resort_name": resort_data["resort_name"]},  # Filter by resort_name
        {"$set": {"resort_name": resort_data["resort_name"], "last_updated": resort_data["last_updated"]}},  # Always update last_updated
        upsert=True  # Insert a new document if none exists
    )

def check_resort_in_resort_cache(resort_name):
    """Retrieve a resort entry from `resorts` cache using unique resort_name."""
    resort = resorts_collection.find_one({"resort_name": resort_name})
    if resort:
        resort.pop("_id", None)  # Remove `_id` for JSON compatibility
    return resort

def save_all_resorts(resort_data):
    """Save a resort entry in `all_resorts` collection with Snow Forecast and Infonieve names."""
    all_resorts_collection.update_one(
        {"resort_name": resort_data["resort_name"]},
        {"$set": resort_data},
        upsert=True
    )

def check_resort_in_all_resorts(resort_name):
    """Retrieve a resort entry from `all_resorts` using unique resort_name."""
    resort = all_resorts_collection.find_one({"resort_name": resort_name})
    if resort:
        resort.pop("_id", None)  # Remove `_id` for JSON compatibility
    return resort

def add_resort_to_all_resorts(resort_data):
    """Add a new resort to `all_resorts` collection or update if it already exists."""
    # Insert or update resort data by `resort_name` to prevent duplicates
    result = all_resorts_collection.update_one(
        {"resort_name": resort_data["resort_name"]},
        {"$set": resort_data},
        upsert=True
    )
    return result.upserted_id or result.matched_count  # Return ID if new, count if updated

def delete_resort_from_all_resorts(resort_name):
    """Delete a resort entry from `all_resorts` collection by resort_name."""
    result = all_resorts_collection.delete_one({"resort_name": resort_name})
    return result.deleted_count > 0  # Return True if a document was deleted, False otherwise

def get_daily_data(resort_name):
    """Retrieve today's data for the specified resort from `daily_data` collection."""
    data = collection.find_one({"resort_name": resort_name})
    if data:
        data.pop("_id", None)  # Remove `_id` for JSON compatibility
    return data