# Snow Advising API Architecture

This document provides an overview of the Snow Advising API architecture, outlining each component, data flow, and key design decisions. The API is designed to collect, process, and serve snow-related data from multiple sources efficiently on a Raspberry Pi.

## 🏗️ System Architecture Overview

The Snow Advising API consists of three main components: 

1. **Data Scraper**
2. **Data Processor**
3. **API Server**

Each component is designed to operate independently and interact efficiently with the others to deliver accurate, real-time data to users.

### Architecture Diagram

Below is an architecture diagram that outlines the data flow between the components and external sources:

```plaintext
Snow Advising API
├── Data Scraper
├── Data Processor
└── API Server

Data Sources
├── snow-forecast.com
├── infonieve.es
└── aemet.es
```

### Data Flow:
1. Data Sources -> Data Scraper (Fetch data daily)
2. Data Scraper -> Data Processor (Process & Clean Data)
3. Data Processor -> Storage (Save Data in SQLite)
4. Storage <-> API Server (Fetch Processed Data)
5. API Server -> Client (Serve Snow Advisories)

### 📦 Component Breakdown
#### 1. Data Scraper
The Data Scraper is responsible for pulling data from snow-forecast.com, infonieve.es, and aemet.es. Each data source has its own scraping module to manage unique data structures and parsing requirements. The scraper uses Python's BeautifulSoup (or Puppeteer for JavaScript-rendered sites if necessary) to parse HTML and extract:
- Snow depth in centimeters
- Weather conditions (temperature, wind speed, and snowfall forecast)
- Runway status for available runs
- To optimize resource usage, scraping is scheduled to run once daily via a Cron job.

#### 2. Data Processor
The Data Processor standardizes and cleans the raw scraped data before storing it. This component reformats data into a consistent structure, validates values (e.g., checking for valid numerical data), and applies any transformation needed for accurate API responses.

The processor stores data in an SQLite database, which is lightweight and ideal for Raspberry Pi. It includes fields like source, date, snow_depth, temperature, wind_speed, and runway_status.

#### 3. API Server
The API Server is a FastAPI-based RESTful interface, exposing endpoints for clients to access the processed data. Key endpoints include:

- `/weather`: Provides the latest weather and snow conditions.
- `/advisory`: Checks if snow depth exceeds a user-defined threshold and returns true or false.

This server interacts with the SQLite database to fetch data, includes basic rate limiting, and implements structured error handling to ensure reliability.

### 📄 Database Schema
The SQLite database schema below captures the snow and weather data structure:

```sql
CREATE TABLE SnowData (
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    snow_depth FLOAT,
    temperature FLOAT,
    wind_speed FLOAT,
    runway_status TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```


### 🔄 Data Flow
1. Data Scraper fetches data from the sources once daily. 
2. Data Processor cleans and standardizes the data, storing it in the SQLite database.
3. API Server retrieves data as requested and serves it to clients through defined endpoints.

### 💡 Design Decisions and Justifications
- SQLite Database: Chosen for its lightweight, low-overhead properties, ideal for Raspberry Pi.
- Modular Scraping: Each data source has a dedicated scraper module, improving maintainability and scalability.
- Scheduled Daily Updates: Limits load on external sources and conserves resources on Raspberry Pi.

### 📈 Future Considerations
- Enhanced Caching: To further optimize performance, consider adding Redis or file-based caching.
- Error Handling and Retries: Expand error handling for cases where data sources are temporarily unavailable.
- Additional Data Sources: Add other reliable snow data providers to improve data accuracy and coverage.
