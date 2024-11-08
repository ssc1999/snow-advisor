# app/api/routes.py
from flask import Blueprint, jsonify
from ..db.mongodb import get_daily_data, save_daily_data
from ..scraper.snow_forecast import scrape_snow_forecast
from ..scraper.infonieve import scrape_infonieve
from ..processor.data_processor import process_data
from datetime import datetime

bp = Blueprint("api", __name__)

@bp.route("/weather/<resort_name>", methods=["GET"])
def get_weather(resort_name):
    # Step 1: Check if data exists in the database
    daily_data = get_daily_data(resort_name)
    
    # Step 2: Check if the data is up-to-date
    if daily_data:
        # If today's data already exists, return it
        if daily_data.get("date") == datetime.utcnow().strftime("%Y-%m-%d"):
            return jsonify(daily_data)

    # Step 3: Scrape data if missing or outdated
    snow_forecast_data = scrape_snow_forecast(resort_name)
    infonieve_data = scrape_infonieve(resort_name)
    
    # Step 4: Merge and format data using the processor
    processed_data = process_data(resort_name, snow_forecast_data, infonieve_data)
    
    if processed_data:
        # Step 5: Save the processed data and return it
        save_daily_data(resort_name, processed_data)
        return jsonify(processed_data)
    
    # Step 6: Return an error if aggregation failed
    return jsonify({"error": f"Data not found and could not scrape for {resort_name}"}), 404

@bp.route("/advisory", methods=["GET"])
def check_advisory():
    # Example logic for advisory endpoint
    snow_depth = 50  # Placeholder value
    threshold = 10  # Replace with threshold logic
    return {"advisory": snow_depth > threshold}
