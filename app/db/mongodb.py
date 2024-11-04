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
    # Find and replace the data with the same resort name
    collection.find_one_and_replace(resort_name, data)

def get_daily_data(resort_name):
    # Default to get the one with the resort name
    return collection.find_one(resort_name)
