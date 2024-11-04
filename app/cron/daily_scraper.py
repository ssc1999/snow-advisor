# app/cron/daily_scraper.py
from scraper.snow_forecast import SnowForecastScraper
from scraper.infonieve import InfonieveScraper
from processor.data_processor import DataProcessor
from db.mongodb import save_daily_data

def daily_scrape():
    snow_forecast_scraper = SnowForecastScraper()
    infonieve_scraper = SnowForecastScraper()
    processor = DataProcessor()
    snow_forecast_raw_data = snow_forecast_scraper.scrape_snow_forecast()
    infonieve_raw_data = infonieve_scraper.scrape_infonieve()
    processed_data = processor.process_data(snow_forecast_raw_data, infonieve_raw_data)

    # Save processed data to MongoDB
    save_daily_data(processed_data)

if __name__ == "__main__":
    daily_scrape()
