import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.scraper.snow_forecast import scrape_weather as snow_forecast_scrape_weather, scrape_resorts_names as snow_forecast_scrape_resorts
from app.scraper.infonieve import scrape_resort_data as infonieve_scrape_resort_data, scrape_resorts_names as infonieve_scrape_resorts


def test_snow_forecast_scrape_resorts():
    """Test scraping list of resorts from snow-forecast.com."""
    resorts = snow_forecast_scrape_resorts()
    assert isinstance(resorts, list)
    assert len(resorts) > 0
    assert all(isinstance(resort, str) for resort in resorts)

def test_infonieve_scrape_resort_data():
    """Test scraping weather data from infonieve.es for a valid resort."""
    resort_name = "sample_resort"
    data = infonieve_scrape_resort_data(resort_name)
    assert data is not None
    assert isinstance(data, dict)
    assert "estado" in data
    assert "calidad" in data

def test_infonieve_scrape_resorts():
    """Test scraping list of resorts from infonieve.es."""
    resorts = infonieve_scrape_resorts()
    assert isinstance(resorts, list)
    assert len(resorts) > 0
    assert all(isinstance(resort, str) for resort in resorts)