import requests
import json
import os
from flask import Flask, jsonify, send_from_directory

# get config values from environment variables
# HOME_LATITUDE, HOME_LONGITUDE, OWM_API_KEY, OWM_UNITS, TEMP_UNIT, FORECAST_ITEMS
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
    lat = os.getenv("HOME_LATITUDE")
    longitude = os.getenv("HOME_LONGITUDE")
    OWM_API_KEY = os.getenv("OWM_API_KEY", "your_api_key")
    OWM_UNITS = os.getenv("OWM_UNITS", "metric")  # Default to metric units
    url = f"{WEATHER_API_URL}/{endpoint}/?lat={lat}&lon={longitude}&appid={OWM_API_KEY}&units={OWM_UNITS}"
    return url


@app.route('/weather', methods=['GET', 'POST'])
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

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def root(path):
    """Serve static files from the 'static' directory."""
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run()