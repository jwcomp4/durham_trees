import dash
from dash import dcc, html, callback, Input, Output, State, Patch
import pandas as pd
import dash_mantine_components as dmc
import plotly.express as px
import json
from utils.data_utils import tree_clean, click_tree_clean
from utils.app_utils import geocode_address, make_card, card_icons
from dash_iconify import DashIconify

dash.register_page(__name__, path="/")

tree = pd.read_csv("tree.csv")

style = {"border": f"1px solid {dmc.DEFAULT_THEME['colors']['indigo'][3]}"}


def layout():
    layout = dmc.Space(h=30), dmc.Grid(
        [
            dmc.Space(w=20),
            dmc.GridCol(
                [
                    dmc.Stack(
                        [
                            dmc.Select(
                                label="Planted Trees or Planting Sites?",
                                id="site-or-tree",
                                data=[
                                    {"value": "Tree", "label": "Tree"},
                                    {
                                        "value": "Planting Site",
                                        "label": "Planting Site",
                                    },
                                ],
                                value="Tree",
                            ),
                            dmc.TextInput(id='address', label="Enter an Address"),
                            dmc.Button(id='address-submit', children="Submit Address")
                        ],
                        gap="xl",
                    )
                ],
                span=3,
                style=style,
            ),
            dmc.GridCol(
                [
                    html.Div(
                        id="graph-container",
                        children=[dcc.Graph(id="tree-map")],
                    ),
                ],
                span=7,
            ),
            dmc.GridCol([dmc.Stack(id='tree-card-stack')], span=4),
            dmc.GridCol([html.Div(id="data-click-div")], span=4),
        ],
        gutter="xl",
    )

    return layout


@callback(Output("tree-map", "figure"), Input("site-or-tree", "value"))
def map_update(value):
    df = tree_clean(value, tree)
    fig = px.scatter_map(
        df,
        lat="Y",
        lon="X",
        map_style="carto-positron",
        hover_data=["genus", "species", "commonname", "diameterin", "plantingdate"],
        zoom=10,
        title="Map of Durham Trees",
    )

    return fig

@callback(Output('tree-map', 'figure', allow_duplicate=True), State('address', 'value'), Input('address-submit', 'n_clicks'), prevent_initial_call=True)
def change_map_center(address, click):
    patch_map = Patch()
    lat, lon = geocode_address(address)
    patch_map['layout']['map']['center']['lat']=lat
    patch_map['layout']['map']['center']['lon']=lon
    patch_map['layout']['map']['zoom']=17
    return patch_map
    



@callback(Output("tree-card-stack", "children"), State('site-or-tree', 'value'), Input("tree-map", "clickData"), prevent_initial_call = True)
def map_click_data(value, click):
    longitude = click['points'][0]['lon']
    latitude = click['points'][0]['lat']
    dff = click_tree_clean(value, tree, latitude, longitude)
    common_name = make_card(card_icons['tree'],dff['commonname'].values[0])
    clicked_diameter = make_card(card_icons['diameter'], dff['diameterin'].values[0])
    planting_date = make_card(card_icons['date'],dff['plantingdate'].values[0])


    
    return [common_name, clicked_diameter, planting_date]


@callback(Output("data-click-div", "children"), Input("tree-map", "selectedData"))
def map_zoom_data(select):
    return json.dumps(select, indent=2)
