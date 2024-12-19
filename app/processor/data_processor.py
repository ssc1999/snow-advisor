import json
from datetime import datetime

class DataProcessor:
    def process_data(self, resort_name, snow_forecast_data, infonieve_data):
        # Check if infonieve_data is a string (JSON) and load it as a dictionary if so
        if isinstance(infonieve_data, str):
            try:
                infonieve_data = json.loads(infonieve_data)
            except json.JSONDecodeError:
                raise ValueError("infonieve_data is not a valid JSON string")

        # Check if snow_forecast_data is a string (JSON) and load it as a dictionary if so
        if isinstance(snow_forecast_data, str):
            try:
                snow_forecast_data = json.loads(snow_forecast_data)
            except json.JSONDecodeError:
                raise ValueError("snow_forecast_data is not a valid JSON string")

        # Use the current date as the default for 'date' field
        date = datetime.now().strftime("%Y-%m-%d")

        # Combine infonieve_data with snow_forecast_data, where snow_forecast_data contains forecasted weather by level
        processed_data = {
            "resort_name": resort_name,
            "date": date,
            "status": infonieve_data.get("status", "N/A"),
            "quality": infonieve_data.get("quality", "N/A"),
            "maximum_thickness": infonieve_data.get("maximum_thickness", "N/A"),
            "minimum_thickness": infonieve_data.get("minimum_thickness", "N/A"),
            "avalanche_risk": infonieve_data.get("avalanche_risk", "N/A"),
            "kilometers": infonieve_data.get("kilometers", "N/A"),
            "slopes": infonieve_data.get("slopes", {}),
            "weather": snow_forecast_data  # Nest the full snow_forecast_data under 'forecast' key
        }

        return processed_data