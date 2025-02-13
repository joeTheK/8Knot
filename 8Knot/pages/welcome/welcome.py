from dash import dcc, html
import dash
import dash_bootstrap_components as dbc
import plotly.express as px

# import other sections
from .sections.general_section import layout as general_tab_contents
from .sections.plotly_section import layout as plotly_tab_contents
from .sections.augur_login_section import layout as augur_tab_contents
from .sections.user_group_section import layout as group_tab_contents

# register the page
dash.register_page(__name__, path="/", order=1)


layout = dbc.Container(
    className="welcome_container",
    children=[
        html.Div(
            className="toplevel_welcome_div",
            children=[
                html.Div(
                    className="welcome_callout_section",
                    children=[
                        html.Img(src="assets/logo-color.png"),
                        html.P(
                            """
                            This is CS4320 FS 2023 Group 8's instance of 8knot for the semester project.
                            """
                        ),
                    ],
                ),
                html.Div(
                    className="welcome_instructions_section",
                    children=[
                        dcc.Tabs(
                            value="general",
                            children=[
                                dcc.Tab(
                                    label="General",
                                    value="general",
                                    children=[general_tab_contents],
                                ),
                                dcc.Tab(
                                    label="Plotly Figure Tools",
                                    value="plotlyfiguretools",
                                    children=[plotly_tab_contents],
                                ),
                                dcc.Tab(
                                    label="Your Augur Account",
                                    value="auguraccount",
                                    children=[augur_tab_contents],
                                ),
                                dcc.Tab(
                                    label="Adding a User Group",
                                    value="usergroup",
                                    children=[group_tab_contents],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ],
)
