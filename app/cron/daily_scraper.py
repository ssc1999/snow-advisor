# app/cron/daily_scraper.py
from scraper.snow_forecast import SnowForecastScraper
from scraper.infonieve import InfonieveScraper
from processor.data_processor import DataProcessor
from datetime import datetime
from db.mongodb import save_daily_data, get_resorts_cache, check_resort_in_all_resorts, save_resort_cache

def daily_scrape():
    resorts = get_resorts_cache()
    for resort in resorts:
        resort_data = check_resort_in_all_resorts(resort["resort_name"])
        
        resort_name = resort_data["resort_name"]
        infonieve_name = resort_data["infonieve_name"]
        snow_forecast_name = resort_data["snow_forecast_name"]
        
        infonieve_scraper = InfonieveScraper(infonieve_name)
        snow_forecast_scraper = SnowForecastScraper(snow_forecast_name)
        processor = DataProcessor()
        
        infonieve_raw_data = infonieve_scraper.scrape_resort_data()
        snow_forecast_raw_data = snow_forecast_scraper.scrape_weather()
        processed_data = processor.process_data(resort_name, snow_forecast_raw_data, infonieve_raw_data)
        
        if processed_data:
        # Attempt to save; only proceed if save is successful
            if not save_daily_data(resort_name, processed_data):
                print(f"Data not found or could not scrape data for {resort_name}")

if __name__ == "__main__":
    daily_scrape()
