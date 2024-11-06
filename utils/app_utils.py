from dotenv import load_dotenv
import os
import requests
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# Loading in environment variable

load_dotenv()

GOOGLE_MAP_KEY = os.environ.get("GOOGLE_MAP_KEY")


def geocode_address(address):
    key = GOOGLE_MAP_KEY
    url_base = "https://maps.googleapis.com/maps/api/geocode/json?address="
    geocode_url = f"{url_base}{address}&key={key}"
    response = requests.get(geocode_url).json()["results"][0]["geometry"]["location"]
    lat = response["lat"]
    lon = response["lng"]
    return lat, lon


def make_card(icon, label, attribute):
    card = dmc.Card(
        [dmc.Group([DashIconify(icon=icon, width=30), dmc.Text(label, fw=700)]), dmc.Text(attribute)],
        withBorder=True,
        shadow="sm",
        radius="md",
    )
    return card

card_attribute = {
    "tree":{"icon":"lucide:trees", "label":"Common Name"},
    "diameter": {"icon":"game-icons:measure-tape", "label":"Diameter (inches)"},
    "date": {"icon":"fluent:calendar-24-regular", "label":"Planting Date"}
}