import dash
from dash import dcc, html, Input, Output, State, Patch
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__, use_pages=True)
server = app.server


