import json
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Mapping for custom weather descriptions
WEATHER_PHRASE_MAPPING = {
    "rain shwrs": "Rain Showers",
    "part cloud": "Partly Cloudy",
    "cloud": "Cloudy",
    "clear": "Clear",
    "light rain": "Light Rain",
    "some clouds": "Some Clouds",
}

def normalize_weather_phrase(phrase):
    """Function to normalize or map raw weather phrases to a more readable format."""
    return WEATHER_PHRASE_MAPPING.get(phrase.lower(), phrase.title())

def get_forecast_dates():
    """Generate dates for the 7-day forecast starting from today."""
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def sanitize_data(value, key=None):
    """Replace empty values or '-' with 'N/A'. Also handles snow and precip separately if specified."""
    if value == "-" or not value:
        return "N/A"
    # Specific handling to replace '-' in 'snow' and 'precip' as "N/A" for clarity
    if key in ["snow", "precip"] and value == "-":
        return "N/A"
    return value

def scrape_snow_forecast(resort_name):
    # Define URLs for different mountain levels
    levels = ["bot", "mid", "top"]
    base_url = f"https://www.snow-forecast.com/resorts/{resort_name}/6day"
    forecast_dates = get_forecast_dates()

    # Main data structure, using OrderedDict to maintain specific order (AM, PM, Night)
    all_data = {
        level: {forecast_dates[day]: OrderedDict([("AM", {}), ("PM", {}), ("Night", {})]) for day in range(7)}
        for level in levels
    }

    # Mapping row types to JSON keys
    row_mapping = {
        "phrases": "weather",
        "wind": "wind",
        "temperature-max": "temp_max",
        "temperature-min": "temp_min",
        "snow": "snow",
        "rain": "precip"
    }
    
    for level in levels:
        url = f"{base_url}/{level}"
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Parse rows of interest
            rows = soup.select("table.forecast-table__table--content tbody tr")
            
            # Fill in data for each day and time period
            for row in rows:
                data_row = row.get("data-row")
                
                if data_row in row_mapping:
                    key = row_mapping[data_row]
                    columns = row.select("td.forecast-table__cell")
                    
                    for day in range(7):
                        try:
                            # Each day has 3 time columns (AM, PM, Night in order)
                            am_data = sanitize_data(columns[day * 3].text.strip(), key=key)  # AM
                            pm_data = sanitize_data(columns[day * 3 + 1].text.strip(), key=key)  # PM
                            night_data = sanitize_data(columns[day * 3 + 2].text.strip(), key=key)  # Night
                            
                            # Normalize weather phrases if the key is "weather"
                            if key == "weather":
                                am_data = normalize_weather_phrase(am_data)
                                pm_data = normalize_weather_phrase(pm_data)
                                night_data = normalize_weather_phrase(night_data)

                            # Populate the OrderedDict in the desired order (AM, PM, Night)
                            all_data[level][forecast_dates[day]]["AM"][key] = am_data
                            all_data[level][forecast_dates[day]]["PM"][key] = pm_data
                            all_data[level][forecast_dates[day]]["Night"][key] = night_data
                        except IndexError:
                            # Handle cases where data is missing by assigning "N/A"
                            all_data[level][forecast_dates[day]]["AM"].setdefault(key, "N/A")
                            all_data[level][forecast_dates[day]]["PM"].setdefault(key, "N/A")
                            all_data[level][forecast_dates[day]]["Night"].setdefault(key, "N/A")

        except requests.RequestException as e:
            print(f"Error fetching data for {level}: {e}")
            all_data[level] = None  # Mark level as unavailable if fetch fails

    # Convert the final output to a JSON string with enforced ordering
    json_data = json.dumps(all_data, ensure_ascii=False, indent=4)
    
    return json_data