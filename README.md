# 🌨️ Snow Advising API

A **Snow Advising API** providing essential snow and weather data to help enthusiasts make informed decisions about winter conditions. Aggregating information from reliable sources like **Snow-Forecast**, **Infonieve**, and **Aemet**, this API supplies real-time data on **snow depth**, **weather conditions**, and **runway availability**—all optimized to run on a **Raspberry Pi**.

## 🔥 Project Overview

In winter sports and travel, accurate snow data is crucial. This project addresses that need by creating a daily-updated, reliable source of snow and weather data—perfect for users planning trips to the mountains. This project showcases advanced **API design**, **web scraping**, and **data processing** in Python, with best practices for efficiency and resource usage.

## 🚀 Features

- **Real-time Snow and Weather Data**: Fetches daily data on snow depth, temperature, wind speed, and more.
- **Advisory Checks**: Easily check if snow depth exceeds a user-defined threshold.
- **Efficient Design**: Optimized to run on low-resource devices like Raspberry Pi with MongoDB for data storage and caching.
- **Modular Architecture**: Clear separation of data scraping, processing, and API serving for easy maintenance.

## 📁 Project Structure

Organized for readability and maintainability, each part of the project is separated into a dedicated module:

```plaintext
snow_advising_api/
├── README.md               # Project overview and setup instructions
├── requirements.txt        # List of dependencies (Flask, BeautifulSoup, etc.)
├── .env                    # Environment variables for API keys, thresholds, etc.
├── config.py               # Configuration file (e.g., paths, constants)
├── main.py                 # Entry point to start the Flask server
├── scraper/                # Folder for web scraping modules
│   ├── base_scraper.py     # Base scraper class with shared methods
│   ├── snow_forecast.py    # Scraper for snow-forecast.com
│   ├── infonieve.py        # Scraper for infonieve.es
│   └── aemet.py            # Scraper for aemet.es
├── processor/              # Folder for data processing and cleaning modules
│   └── data_processor.py   # Module to clean, transform, and standardize data
├── db/                     # Database management
│   ├── mongodb.py          # MongoDB connection and helper functions
├── api/                    # API endpoints
│   ├── advisory/           # Advisory-related routes
│   │   └── routes.py       # Advisory endpoint definitions
│   ├── resorts/            # Resorts-related routes
│   │   └── routes.py       # Resorts management endpoints
│   ├── weather/            # Weather-related routes
│   │   └── routes.py       # Weather endpoint definitions
│   └── __init__.py         # Registering blueprints for the Flask app
├── cron/                   # Folder for scheduled job scripts
│   └── daily_scraper.py    # Script to scrape data daily (invoked by Cron)
├── tests/                  # Unit test files
│   ├── test_scrapers.py    # Tests for individual scrapers
│   ├── test_processor.py   # Tests for data processor
│   └── test_api.py         # Tests for API endpoints
└── docs/                   # Project documentation (Markdown)
    └── architecture.md     # Architecture and design documentation
```

## 🛠️ Setup & Installation

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/snow-advising-api.git
cd snow-advising-api
```

### 2. Create and Activate a Virtual Environment:
Create a virtual environment to isolate dependencies.

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```
### 3.Install Dependencies: Install all required dependencies listed in requirements.txt:
```bash
pip install -r requirements.txt
```

### 4.Set Up Environment Variables: Copy the .env.example file to .env and fill in any necessary API keys and configurations.
```bash
cp .env.example .env
```
### 5. Initialize the MongoDB Database
Ensure MongoDB is running on your machine or a remote server and that the connection details in .env are correct.

### 6.Run the Flask Server
Start the API server locally:
```bash
flask run
```
### 7.Set Up Daily Data Scraping: 
To automatically update snow and weather data daily, use Cron to schedule the daily_scraper.py script. Edit your crontab file:
```bash
crontab -e
```
### 8.Add the following line to your crontab file if you're using crontab:
```bash
0 6 * * * /usr/bin/python3 /path/to/daily_scraper.py
```

## Your Snow Advising API is now set up and ready to use!

## 📊 Endpoints
| Endpoint             | Method | Description                                                |
|----------------------|--------|------------------------------------------------------------|
| `/weather/<resort_name>` | GET    | Fetches current snow and weather data for a specified resort. |
| `/advisory`          | GET    | Checks if the snow depth exceeds a predefined threshold.   |
| `/resorts/all`       | GET    | Retrieves all resorts listed in the `all_resorts` collection. |
| `/resorts/cache`     | GET    | Retrieves cached resorts data from the `resorts` collection. |
| `/resorts/add`       | POST   | Adds or updates a resort in the `all_resorts` collection.  |

## 🛠️ Technology Stack
- Python: Core programming language for backend development.
- Flask: Lightweight framework for RESTful API development.
- MongoDB: NoSQL database used for data storage.
- BeautifulSoup & Requests: Web scraping tools for gathering snow data
- Cron: Automated scheduling of daily scraping tasks.

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