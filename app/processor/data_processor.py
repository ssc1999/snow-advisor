import json
from datetime import datetime

class DataProcessor:
    def process_data(resort_name, snow_forecast_data, infonieve_data):
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
            "estado": infonieve_data.get("estado", "N/A"),
            "calidad": infonieve_data.get("calidad", "N/A"),
            "espesor_maximo": infonieve_data.get("espesor_maximo", "N/A"),
            "espesor_minimo": infonieve_data.get("espesor_minimo", "N/A"),
            "peligro_de_aludes": infonieve_data.get("peligro_de_aludes", "N/A"),
            "kilometros": infonieve_data.get("kilometros", "N/A"),
            "pistas": infonieve_data.get("pistas", {}),
            "weather": snow_forecast_data  # Nest the full snow_forecast_data under 'forecast' key
        }

        return processed_data