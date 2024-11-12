import os
import json
import openai
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.mongodb import save_all_resorts
from app.scraper.snow_forecast import scrape_resorts_names as scrape_resorts_snow_forecast
from app.scraper.infonieve import scrape_resorts_names as scrape_resorts_infonieve

# Initialize the OpenAI client
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_standardized_resort_names(snow_forecast_resorts, infonieve_resorts):
    prompt = f"""
    I have two lists of ski resorts from two different sources: snow-forecast.com and infonieve.es.
    Please match the resort names from each source where possible and suggest a standardized name for each resort.

    Here are the lists:
    
    Snow Forecast Resorts: {snow_forecast_resorts}
    Infonieve Resorts: {infonieve_resorts}

    Return a JSON array where each item has the following structure:
    {{
        "resort_name": "<standardized name>",
        "snow_forecast_name": "<name from snow-forecast.com or null if unmatched>",
        "infonieve_name": "<name from infonieve.es or null if unmatched>"
    }}
    """

    try:
        print("Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.3,
        )
        # Parse response as JSON
        matched_resorts = json.loads(response.choices[0].message.content)
        print("Resort names matched successfully.")
        return matched_resorts
    except openai.APIError as e:
        print(f"Error from ChatGPT API: {e}")
        return None

def initialize_all_resorts():
    print("Scraping Snow Forecast resorts...")
    snow_forecast_resorts = scrape_resorts_snow_forecast()
    print("Scraping Infonieve resorts...")
    infonieve_resorts = scrape_resorts_infonieve()
    
    print("Matching resorts using ChatGPT...")
    matched_resorts = get_standardized_resort_names(snow_forecast_resorts, infonieve_resorts)

    if matched_resorts:
        for resort in matched_resorts:
            save_all_resorts(resort)
        print("All resorts have been initialized and saved.")
    else:
        print("Failed to retrieve or parse standardized resorts data from ChatGPT.")

# Run the function
if __name__ == "__main__":
    initialize_all_resorts()