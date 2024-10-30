import dash
from dash import dcc, html, callback, Input, Output, State, Patch
import pandas as pd
import dash_mantine_components as dmc
import plotly.express as px
import json
from utils.data_utils import tree_clean
from utils.app_utils import geocode_address

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
            dmc.GridCol([html.Div(id="data-div")], span=4),
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
    



@callback(Output("data-div", "children"), Input("tree-map", "relayoutData"))
def map_zoom_data(relayout):
    return json.dumps(relayout, indent=2)


@callback(Output("data-click-div", "children"), Input("tree-map", "selectedData"))
def map_zoom_data(select):
    return json.dumps(select, indent=2)
