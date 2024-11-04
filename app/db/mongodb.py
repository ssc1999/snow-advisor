# app/db/mongodb.py
import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["snow_advising"]
collection = db["daily_data"]

def save_daily_data(data):
    # Add a timestamp for when the data is stored
    data["date"] = datetime.utcnow().strftime("%Y-%m-%d")
    collection.insert_one(data)

def get_daily_data(date=None):
    if date:
        return collection.find_one({"date": date})
    # Default to get the latest record
    return collection.find().sort("date", -1).limit(1)
