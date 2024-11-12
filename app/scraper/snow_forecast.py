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
    """Normalize raw weather phrases to a readable format."""
    return WEATHER_PHRASE_MAPPING.get(phrase.lower(), phrase.title())

def get_forecast_dates():
    """Generate dates for the 7-day forecast starting from today."""
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def sanitize_data(value):
    """Replace empty values or '-' with 'N/A'."""
    return "N/A" if value == "-" or not value else value

def scrape_weather(resort_name):
    levels = ["bot", "mid", "top"]
    base_url = f"https://www.snow-forecast.com/resorts/{resort_name}/6day"
    forecast_dates = get_forecast_dates()

    # Initialize final data structure
    all_data = OrderedDict()
    
    # Mapping table rows to keys
    row_mapping = {
        "phrases": "weather",
        "wind": "wind",
        "temperature-max": "temp_max",
        "temperature-min": "temp_min",
        "snow": "snow",
        "rain": "precip"
    }

    for level in levels:
        level_data = OrderedDict()
        for day in forecast_dates:
            level_data[day] = {
                "AM": OrderedDict(),
                "PM": OrderedDict(),
                "Night": OrderedDict()
            }

        try:
            url = f"{base_url}/{level}"
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.select("table.forecast-table__table--content tbody tr")

            for row in rows:
                data_row = row.get("data-row")
                if data_row in row_mapping:
                    key = row_mapping[data_row]
                    columns = row.select("td.forecast-table__cell")

                    for day_idx, day in enumerate(forecast_dates):
                        try:
                            am_data = sanitize_data(columns[day_idx * 3].text.strip())
                            pm_data = sanitize_data(columns[day_idx * 3 + 1].text.strip())
                            night_data = sanitize_data(columns[day_idx * 3 + 2].text.strip())

                            if key == "weather":
                                am_data = normalize_weather_phrase(am_data)
                                pm_data = normalize_weather_phrase(pm_data)
                                night_data = normalize_weather_phrase(night_data)

                            # Populate data directly in the correct structure
                            level_data[day]["AM"][key] = am_data
                            level_data[day]["PM"][key] = pm_data
                            level_data[day]["Night"][key] = night_data
                        except IndexError:
                            # Assign "N/A" for missing data
                            for period in ["AM", "PM", "Night"]:
                                level_data[day][period].setdefault(key, "N/A")

        except requests.RequestException as e:
            print(f"Error fetching data for {level}: {e}")
            all_data[level] = None
            continue

        # Finalize level data in `all_data`
        all_data[level] = level_data

    # Convert to JSON with strict order
    return json.dumps(all_data, ensure_ascii=False, indent=4)

def scrape_resorts_names():
    url = "https://www.snow-forecast.com/sitemap.xml"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'xml')
    resorts = set()

    for loc in soup.find_all("loc"):
        url = loc.text
        if "/resorts/" in url and url.count("/") == 5:
            resort_name = url.split("/")[4]
            resorts.add(resort_name)

    return list(resorts)