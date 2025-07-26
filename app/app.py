import requests
import json
import os
from flask import Flask, jsonify

# get config values from environment variables
# OWM_CITY_ID, OWM_API_KEY, OWM_UNITS, TEMP_UNIT, FORECAST_ITEMS
# are expected to be set in the environment
# or in a env.sample file loaded by dotenv
from dotenv import load_dotenv
load_dotenv()

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5"
TEMP_UNIT = os.getenv("TEMP_UNIT", "C")  # Default temperature unit
FORECAST_ITEMS = int(os.getenv("FORECAST_ITEMS", 5))

app = Flask(__name__)

def get_request_url(endpoint):
    """Constructs the full URL for the OpenWeatherMap API request."""
    OWM_CITY_ID = os.getenv("OWM_CITY_ID", "your_city_id")
    OWM_API_KEY = os.getenv("OWM_API_KEY", "your_api_key")
    OWM_UNITS = os.getenv("OWM_UNITS", "metric")  # Default to metric units
    url = f"{WEATHER_API_URL}/{endpoint}/?id={OWM_CITY_ID}&appid={OWM_API_KEY}&units={OWM_UNITS}"
    return url


@app.route('/weather')
def weather():
    current = requests.get(get_request_url("weather")).json()
    forecast = requests.get(get_request_url("forecast")).json()

    data = {
        'current': current,
        'forecast': forecast,
        'tempUnit': TEMP_UNIT,
        'forecastItems': FORECAST_ITEMS
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()