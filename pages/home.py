import dash 
from dash import dcc, html, callback, Input, Output, State
import pandas as pd
import dash_mantine_components as dmc
import plotly.express as px
from utils.data_utils import tree_clean

dash.register_page(__name__, path='/')

tree = pd.read_csv("tree.csv")

def layout():
    layout = dmc.Container(
        [
            dmc.Flex(
                [
                    dmc.TextInput(label="Enter an Address"),
                    dmc.Select(
                        label="Planted Trees or Planting Sites?",
                        id="site-or-tree",
                        data=[
                            {"value":"Tree", "label":"Tree"},
                            {"value":"Planting Site", "label":"Planting Site"},
                        ],
                        
                    ), 
                    dmc.Container(
                        [
                            dcc.Graph(id='tree-map')
                        ]
                        )
                ], align='center', justify='flex-start', gap={"base":"sm"}
            )
        ]
    )
    return layout

@callback(
    Output('tree-map', 'figure'),
    Input('site-or-tree', 'value')
)
def map_update(value):
    df = tree_clean(value, tree)
    fig = px.scatter_map(df, lat="Y", lon="X", map_style='carto-positron',
                             hover_data=['genus','species', 'commonname', 'diameterin', 'plantingdate'], zoom=10)
    return fig