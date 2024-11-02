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


def make_card(icon, attribute):
    card = dmc.Card(
        [dmc.Group([DashIconify(icon=icon, width=30), dmc.Text(attribute)])],
        withBorder=True,
        shadow="sm",
        radius="md",
    )
    return card

card_icons = {
    "tree": "lucide:trees",
    "diameter": "game-icons:measure-tape",
    "date": "fluent:calendar-24-regular"
}

