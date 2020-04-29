"""
Dash App Module.
"""
import pandas as pd

import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from flask import Flask

from app.plotly_dash.constants import Colors, DASH_APP_PREFIX
from app.plotly_dash.layouts.lines import get_lines_page_layout
from app.plotly_dash.layouts.profile import get_profile_graph_layout


def init_plotly_dash(app: Flask):
    """ Create a Plotly Dash dashboard. """
    with app.app_context():
        dash_app = dash.Dash(
            server=app,
            routes_pathname_prefix=DASH_APP_PREFIX,
            external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
        )
        app_setup(dash_app)
        app = dash_app.server


def app_setup(dash_app):
    dash_app.config.suppress_callback_exceptions = True
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', style={'color': Colors.TEXT})
    ])

    lines_graph_layout = get_lines_page_layout(dash_app)
    profile_graph_layout = get_profile_graph_layout(dash_app)

    @dash_app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')],
    )
    def display_page(pathname):
        if pathname == f'{DASH_APP_PREFIX}lines/':
            return lines_graph_layout
        if pathname == f'{DASH_APP_PREFIX}profile/':
            return profile_graph_layout
        else:
            return '404'
