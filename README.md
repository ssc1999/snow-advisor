# 🌨️ Snow Advising API

A **Snow Advising API** that provides essential snow and weather data to help enthusiasts make informed decisions about winter conditions. Aggregating information from reliable sources like **Snow-Forecast**, **Infonieve**, and **Aemet**, this API supplies real-time data on **snow depth**, **weather conditions**, and **runway availability**—all optimized to run on a **Raspberry Pi**.

## 🔥 Project Overview

In winter sports and travel, accurate snow data is crucial. This project tackles that need by creating a daily-updated, reliable source of snow and weather data—perfect for users planning their trips to the mountains. This project showcases advanced **API design**, **web scraping**, and **data processing** in Python, with best practices for efficiency and resource usage.

## 🚀 Features

- **Real-time Snow and Weather Data**: Fetches daily data on snow depth, temperature, wind speed, and more.
- **Advisory Checks**: Easily check if snow depth exceeds a user-defined threshold.
- **Efficient Design**: Optimized to run on low-resource devices like Raspberry Pi with SQLite storage and caching.
- **Modular Architecture**: Clear separation of data scraping, processing, and API serving for easy maintenance.

## 📁 Project Structure

Organized for readability and maintainability, each part of the project is separated into a dedicated module:

```plaintext
snow_advising_api/
├── README.md               # Project overview and setup instructions
├── requirements.txt        # List of dependencies (FastAPI, BeautifulSoup, etc.)
├── .env                    # Environment variables for API keys, thresholds, etc.
├── config.py               # Configuration file (e.g., paths, constants)
├── main.py                 # Entry point to start the FastAPI server
├── scraper/                # Folder for web scraping modules
│   ├── base_scraper.py     # Base scraper class with shared methods
│   ├── snow_forecast.py    # Scraper for snow-forecast.com
│   ├── infonieve.py        # Scraper for infonieve.es
│   └── aemet.py            # Scraper for aemet.es
├── processor/              # Folder for data processing and cleaning modules
│   └── data_processor.py   # Module to clean, transform, and standardize data
├── db/                     # Database management
│   ├── database.py         # Database connection and helper functions
│   └── models.py           # Database models (e.g., SQLAlchemy ORM classes)
├── api/                    # API endpoints
│   ├── routes.py           # FastAPI route definitions
│   └── utils.py            # Utility functions for validation, rate limiting, etc.
├── cron/                   # Folder for scheduled job scripts
│   └── daily_scraper.py    # Script to scrape data daily (invoked by Cron)
├── tests/                  # Unit test files
│   ├── test_scrapers.py    # Tests for individual scrapers
│   ├── test_processor.py   # Tests for data processor
│   └── test_api.py         # Tests for API endpoints
└── docs/                   # Project documentation (Markdown)
    └── architecture.md     # Architecture and design documentation
```

## ⚙️ Setup & Installation
Clone the Repository:
```bash
git clone https://github.com/yourusername/snow-advising-api.git
cd snow-advising-api
```
Install Dependencies: Install all required dependencies listed in requirements.txt:
```bash
pip install -r requirements.txt
Set Up Environment Variables: Copy the .env.example file to .env and fill in any necessary API keys and configurations.
```
Run the FastAPI Server: Start the API server locally:
```bash
uvicorn main:app --reload
```
Set Up Daily Data Scraping: Schedule the daily_scraper.py script using Cron:
```bash
0 6 * * * /usr/bin/python3 /path/to/daily_scraper.py
```

## 📊 Endpoints
| Endpoint    | Method | Description                                       |
|-------------|--------|---------------------------------------------------|
| `/weather`  | GET    | Fetches current snow and weather data             |
| `/advisory` | GET    | Checks if snow depth exceeds a specified threshold|


## 🛠️ Technology Stack
- Python: Core programming language
- FastAPI: For creating fast and easy RESTful APIs
- SQLite: Lightweight database for data storage on Raspberry Pi
- BeautifulSoup & Requests: Web scraping tools for gathering snow data
- Cron: For daily data scraping tasks

## 🧪 Tests
Run all tests to ensure each component works as expected:

```bash
pytest tests/
```

## 🧪 Tests
Run all tests to ensure each component works as expected:

```bash
pytest tests/
```

## 🔗 Future Improvements
Enhanced Caching: Further reduce load on sources by implementing a more advanced caching strategy.
Error Resilience: Expand error handling for better resilience to data source downtime.
Historical Data Analysis: Provide insights on past snow data and trends.

## 📜 License
This project is licensed under the MIT License. Feel free to use and modify it as needed.