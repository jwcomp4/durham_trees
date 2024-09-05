import dash
from dash import dcc, html, Input, Output, State, Patch
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px


# setting react version to use latest dmc
dash._dash_renderer._set_react_version("18.2.0")


app = dash.Dash(__name__, use_pages=True)
server = app.server


tree = pd.read_csv("tree.csv")

app.layout = (
    dmc.MantineProvider(
        dmc.AppShell(
            [
                dmc.AppShellHeader(
                    children=[
                        dmc.Title(children=["Durham Trees"], order=1),
                        dmc.Menu(
                            [
                                dmc.MenuTarget(
                                    dmc.Burger(opened=False),
                                ),
                                dmc.MenuDropdown(
                                    [
                                        dmc.MenuItem(
                                            f"{page['name']}",
                                            href=page["relative_path"],
                                        )
                                        for page in dash.page_registry.values()
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            ],
            header={"height": 85},
            zIndex=1400,
        ),
    ),
)
dash.page_container


if __name__ == "__main__":
    app.run(debug=True)
