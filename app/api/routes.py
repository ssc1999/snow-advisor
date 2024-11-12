# app/api/routes.py
from flask import Blueprint, jsonify
from ..db.mongodb import get_daily_data, get_all_resorts, get_resorts_cache, save_daily_data, save_resort_cache, check_resort_in_all_resorts, check_resort_in_resort_cache
from ..scraper.snow_forecast import scrape_weather as snow_forecast_scrape_weather, scrape_resorts_names as snow_forecast_scrape_resort_names
from ..scraper.infonieve import scrape_resort_data as infonieve_scrape_resort_data, scrape_resorts_names as infonieve_scrape_resort_names
from ..processor.data_processor import process_data
from datetime import datetime

bp = Blueprint("api", __name__)

# TODO create endpoint to get all resorts from infonieve and snow forecast, and then mixing them maybe with AI, at least one manually if necessary

@bp.route("/weather/<resort_name>", methods=["GET"])
def get_weather(resort_name):
    # Step 1: Check if the resort exists in `all_resorts` collection
    all_resort_entry = check_resort_in_all_resorts(resort_name)
    if not all_resort_entry:
        return jsonify({"error": f"No standardized entry found for {resort_name}"}), 404

    standardized_name = all_resort_entry["resort_name"]
    
    # Step 2: Check if today's data already exists in `daily_data` collection
    daily_data = get_daily_data(standardized_name)
    today_date = datetime.utcnow().strftime("%Y-%m-%d")
    if daily_data and daily_data.get("date") == today_date:
        return jsonify(daily_data)

    # Step 3: Scrape new data if cache is missing or outdated
    snow_forecast_data = snow_forecast_scrape_weather(all_resort_entry["snow_forecast_name"])
    infonieve_data = infonieve_scrape_resort_data(all_resort_entry["infonieve_name"])
    
    # Step 4: Process and merge the scraped data
    processed_data = process_data(standardized_name, snow_forecast_data, infonieve_data)
    if processed_data:
        # Save processed data to `resorts` cache with `last_updated` as today
        processed_data["last_updated"] = today_date
        save_resort_cache({"resort_name": standardized_name, "last_updated": today_date})
        
        # Save the daily data separately to `daily_data` collection
        processed_data["date"] = today_date
        save_daily_data(standardized_name, processed_data)
        
        return jsonify(processed_data)
    
    return jsonify({"error": f"Data not found or could not scrape data for {resort_name}"}), 404

@bp.route("/advisory", methods=["GET"])
def check_advisory():
    # Example logic for advisory endpoint
    snow_depth = 50  # Placeholder value
    threshold = 10  # Replace with threshold logic
    return {"advisory": snow_depth > threshold}

@bp.route("/all_resorts", methods=["GET"])
def fetch_all_resorts():
    """Fetch all resorts from `all_resorts` collection."""
    all_resorts = get_all_resorts()
    return jsonify(all_resorts), 200

@bp.route("/resorts_cache", methods=["GET"])
def fetch_resorts():
    """Fetch all resorts from `resorts` collection."""
    resorts = get_resorts_cache()
    return jsonify(resorts), 200

@bp.route("/add_resort", methods=["POST"])
def add_resort():
    # Parse the request data as JSON
    resort_data = request.get_json()
    
    # Validate required fields in the request
    if not resort_data or "resort_name" not in resort_data:
        return jsonify({"error": "Invalid input. 'resort_name' is required."}), 400

    # Call the function to add resort to `all_resorts`
    result = add_resort_to_all_resorts(resort_data)
    
    # Check if result indicates a new insert or an update
    if result:
        return jsonify({"message": "Resort added or updated successfully.", "result": str(result)}), 201
    else:
        return jsonify({"message": "No change made."}), 200