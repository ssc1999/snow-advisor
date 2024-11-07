import json
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup

def scrape_snow_forecast(resort_name):
    # Define URLs for different mountain levels
    levels = ["bot", "mid", "top"]
    base_url = f"https://www.snow-forecast.com/resorts/{resort_name}/6day"

    # Main data structure, using OrderedDict to maintain specific order (AM, PM, Night)
    all_data = {
        level: {str(day): OrderedDict([("AM", {}), ("PM", {}), ("Night", {})]) for day in range(7)}
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
                        # Each day has 3 time columns (AM, PM, Night in order)
                        try:
                            am_data = columns[day * 3].text.strip()  # AM
                            pm_data = columns[day * 3 + 1].text.strip()  # PM
                            night_data = columns[day * 3 + 2].text.strip()  # Night
                            
                            # Populate the OrderedDict in the desired order (AM, PM, Night)
                            all_data[level][str(day)]["AM"][key] = am_data
                            all_data[level][str(day)]["PM"][key] = pm_data
                            all_data[level][str(day)]["Night"][key] = night_data
                        except IndexError:
                            # Handle cases where data is missing
                            pass

        except requests.RequestException as e:
            print(f"Error fetching data for {level}: {e}")
            all_data[level] = None  # Mark level as unavailable if fetch fails

    # Convert the final output to a JSON string with enforced ordering
    json_data = json.dumps(all_data, ensure_ascii=False, indent=4)
    
    return json_data