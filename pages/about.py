import dash 
from dash import dcc, html, callback, Input, Output, State

dash.register_page(__name__)

def layout():
    layout = html.Div()
    return layout