from flask import Blueprint, jsonify
from ...db.mongodb import get_daily_data, save_daily_data, save_resort_cache, check_resort_in_all_resorts
from ...scraper.snow_forecast import scrape_weather as snow_forecast_scrape_weather
from ...scraper.infonieve import scrape_resort_data as infonieve_scrape_resort_data
from ...processor.data_processor import process_data
from datetime import datetime

bp = Blueprint("weather", __name__)

@bp.route("/<resort_name>", methods=["GET"])
def get_weather(resort_name):
    all_resort_entry = check_resort_in_all_resorts(resort_name)
    if not all_resort_entry:
        return jsonify({"error": f"No resort found with the name: {resort_name}"}), 404

    standardized_name = all_resort_entry["resort_name"]
    daily_data = get_daily_data(standardized_name)
    
    if daily_data:
        return jsonify(daily_data)

    snow_forecast_data = snow_forecast_scrape_weather(all_resort_entry["snow_forecast_name"])
    infonieve_data = infonieve_scrape_resort_data(all_resort_entry["infonieve_name"])
    processed_data = process_data(standardized_name, snow_forecast_data, infonieve_data)

    if processed_data:
        save_daily_data(standardized_name, processed_data)
        return jsonify(processed_data)

    return jsonify({"error": f"Data not found or could not scrape data for {resort_name}"}), 404