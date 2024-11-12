# app/cron/daily_scraper.py
from scraper.snow_forecast import SnowForecastScraper
from scraper.infonieve import InfonieveScraper
from processor.data_processor import DataProcessor
from db.mongodb import save_daily_data, get_resorts_cache

def daily_scrape():
    resorts = get_resorts_cache()
    for resort in resorts:
        resort_name = resort["resort_name"]
        snow_forecast_scraper = SnowForecastScraper(resort_name)
        infonieve_scraper = InfonieveScraper(resort_name)
        processor = DataProcessor()
        snow_forecast_raw_data = snow_forecast_scraper.scrape_weather()
        infonieve_raw_data = infonieve_scraper.scrape_resort_data()
        processed_data = processor.process_data(resort_name, snow_forecast_raw_data, infonieve_raw_data)
        
        if processed_data:
        # Attempt to save; only proceed if save is successful
            if not save_daily_data(resort_name, processed_data):
                return jsonify({"error": f"Data not found or could not scrape data for {resort_name}"}), 404

if __name__ == "__main__":
    daily_scrape()
# TODO add a cron job to run this every day at midnight
# TODO add logger
