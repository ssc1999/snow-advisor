# app/db/mongodb.py
from pymongo import MongoClient, ASCENDING
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["snow_advising"]
collection = db["daily_data"]

# Ensure resort_name is unique
collection.create_index([("resort_name", ASCENDING)], unique=True)

def save_daily_data(resort_name, data):
    # Remove existing "date" field if present to avoid creating duplicates on update
    data.pop("date", None)
    # Add current timestamp only if we’re inserting fresh data
    data["date"] = datetime.utcnow().strftime("%Y-%m-%d")
    
    # Upsert by resort_name, replace if exists, or insert new if not
    collection.find_one_and_replace(
        {"resort_name": resort_name},  # Filter by resort name
        data,                           # Data to replace or insert
        upsert=True                     # Insert if not found
    )

def get_daily_data(resort_name):
    # Retrieve the data from the database
    data = collection.find_one({"resort_name": resort_name})
    if data:
        # Remove the `_id` field as it is not JSON serializable
        data.pop("_id", None)
    return data