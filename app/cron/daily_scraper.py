from scraper.snow_forecast import SnowForecastScraper
from scraper.infonieve import InfonieveScraper
from processor.data_processor import DataProcessor
from db.mongodb import save_daily_data, get_resorts_cache, check_resort_in_all_resorts
from datetime import datetime

def daily_scrape():
    resorts = get_resorts_cache()
    for resort in resorts:
        try:
            # Check if the resort exists in all_resorts
            resort_data = check_resort_in_all_resorts(resort["resort_name"])
            if not resort_data:
                print(f"Resort {resort['resort_name']} not found in all_resorts.")
                continue

            resort_name = resort_data["resort_name"]
            infonieve_name = resort_data.get("infonieve_name")
            snow_forecast_name = resort_data.get("snow_forecast_name")

            # Initialize scrapers and processor
            infonieve_scraper = InfonieveScraper(infonieve_name)
            snow_forecast_scraper = SnowForecastScraper(snow_forecast_name)
            processor = DataProcessor()

            # Fetch raw data
            infonieve_raw_data = infonieve_scraper.scrape_resort_data()
            snow_forecast_raw_data = snow_forecast_scraper.scrape_weather()

            # Process data
            processed_data = processor.process_data(resort_name, snow_forecast_raw_data, infonieve_raw_data)
            if processed_data:
                if save_daily_data(resort_name, processed_data):
                    print(f"Data for {resort_name} saved successfully.")
                else:
                    print(f"Failed to save data for {resort_name}.")
            else:
                print(f"No data processed for {resort_name}.")

        except Exception as e:
            print(f"Error processing resort {resort['resort_name']}: {e}")

if __name__ == "__main__":
    daily_scrape()