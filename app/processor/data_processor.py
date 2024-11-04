# app/processor/data_processor.py

def process_data(snow_forecast_data, infonieve_data):
    if not snow_forecast_data or not infonieve_data:
        return None

    # Assume the latest date is used if dates differ slightly
    date = snow_forecast_data.get("date") or infonieve_data.get("date")
    
    # Merge data from both sources
    processed_data = {
        "resort": snow_forecast_data.get("resort"),
        "date": date,
        "weather": {
            # Example: Averaging temperature, taking max snow depth, etc.
            "temperature": (
                (snow_forecast_data.get("temperature") or 0) + (infonieve_data.get("temperature") or 0)
            ) / 2,
            "snow_depth": max(snow_forecast_data.get("snow_depth", 0), infonieve_data.get("snow_depth", 0)),
            "wind_speed": snow_forecast_data.get("wind_speed") or infonieve_data.get("wind_speed")
        },
        "advisory": {
            "snow_depth_threshold": 30,
            "advisory_status": max(
                snow_forecast_data.get("snow_depth", 0), infonieve_data.get("snow_depth", 0)
            ) > 30
        },
        "runway_status": snow_forecast_data.get("runway_status") or infonieve_data.get("runway_status")
    }

    return processed_data
