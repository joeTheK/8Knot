from dash import html
import dash
import dash_bootstrap_components as dbc

# register the page
dash.register_page(__name__)

layout = dbc.Container(
    [
        dbc.Row([dbc.Col([html.H1(children="CI/CD")])]),
    ],
    fluid=True,
)
