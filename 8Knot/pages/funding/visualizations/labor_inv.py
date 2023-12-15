from dash import html, dcc, callback
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
import logging
from dateutil.relativedelta import *  # type: ignore
import plotly.express as px
from pages.utils.graph_utils import get_graph_time_values, color_seq
from queries.labor_inv_query import labor_inv_query as liq
from pages.utils.job_utils import nodata_graph
from cache_manager.cache_manager import CacheManager as cm
import io
import time

PAGE = "funding"
VIZ_ID = "labor_inv"


gc_labor_inv = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H3(
                    "Labor Investment",
                    className="card-title",
                    style={"textAlign": "center"},
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("Graph Info:"),
                        dbc.PopoverBody(
                            """
                            Visualizes growth of Issue backlog. Differentiates sub-populations\n
                            of issues by their 'Staleness.'\n
                            Please see the definition of 'Staleness' on the Info page.
                            """
                        ),
                    ],
                    id=f"popover-{PAGE}-{VIZ_ID}",
                    target=f"popover-target-{PAGE}-{VIZ_ID}",
                    placement="top",
                    is_open=False,
                ),
                dcc.Loading(
                    dcc.Graph(id=f"{PAGE}-{VIZ_ID}"),
                ),
                dbc.Form(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "About Graph",
                                        id=f"popover-target-{PAGE}-{VIZ_ID}",
                                        color="secondary",
                                        size="sm",
                                    ),
                                    width="auto",
                                    style={"paddingTop": ".5em"},
                                ),
                            ],
                            align="center",
                            justify="between",
                        ),
                    ]
                ),
            ]
        )
    ],
)


# callback for graph info popover
@callback(
    Output(f"popover-{PAGE}-{VIZ_ID}", "is_open"),
    [Input(f"popover-target-{PAGE}-{VIZ_ID}", "n_clicks")],
    [State(f"popover-{PAGE}-{VIZ_ID}", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output(f"{PAGE}-{VIZ_ID}", "figure"),
    [
        Input("repo-choices", "data"),
    ],
    background=True,
)
def new_staling_issues_graph(repolist):

    # wait for data to asynchronously download and become available.
    cache = cm()
    df = cache.grabm(func=liq, repos=repolist)
    while df is None:
        time.sleep(1.0)
        df = cache.grabm(func=liq, repos=repolist)

    start = time.perf_counter()
    logging.warning(f"{VIZ_ID} - START")

    # test if there is data
    if df.empty:
        logging.warning(f"{VIZ_ID} - NO DATA AVAILABLE")
        return nodata_graph, False

    # function for all data pre processing
    df_status = process_data(df)

    fig = create_figure(df_status)

    logging.warning(f"{VIZ_ID} - END - {time.perf_counter() - start}")
    return fig


def process_data(df: pd.DataFrame):
    return df


def create_figure(df_status: pd.DataFrame):
    # Make a bar graph
    top_companies = df_status.groupby("company")["count"].sum().nlargest(10).reset_index()
    fig = px.bar(
        top_companies,
        x="company",  # Using "id" instead of "repo_id" as per the SELECT statement
        y="count",
        #color="company",  # Using "company" instead of "cntrb_company"
        labels={"count": "Line Count", "company": "Company"},
        title="Top 10 Labor Investment by Company",
    )

    # Edit hover values
    fig.update_traces(
        hovertemplate="Company: %{x}<br>Count: %{y}<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="Company",
        yaxis_title="Count",
        font=dict(size=14),
        #legend_title="Company",
        yaxis=dict(range=[0, None]),
        #yaxis=dict(fixedrange=True),
    )

    return fig

