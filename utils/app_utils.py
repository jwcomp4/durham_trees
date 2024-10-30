from dotenv import load_dotenv
import os
import requests

# Loading in environment variable

load_dotenv()

GOOGLE_MAP_KEY = os.environ.get("GOOGLE_MAP_KEY")

def geocode_address(address):
    key = GOOGLE_MAP_KEY
    url_base = "https://maps.googleapis.com/maps/api/geocode/json?address="
    geocode_url = f"{url_base}{address}&key={key}"
    response = requests.get(geocode_url).json()['results'][0]['geometry']['location']
    lat = response['lat']
    lon = response['lng']
    return lat, lon
    