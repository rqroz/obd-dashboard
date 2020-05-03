"""
Dash App Module.
"""
import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from flask import Flask

from app.utils.auth import AuthHandler, AuthHandlerException

from app.plotly_dash.constants import DASH_APP_PREFIX

from app.plotly_dash.callbacks.lines import register_line_graph_callbacks
from app.plotly_dash.callbacks.profile import register_radar_callbacks
from app.plotly_dash.layouts.lines import get_lines_page_layout
from app.plotly_dash.layouts.profile import get_profile_graph_layout


def init_plotly_dash(app: Flask):
    """
    Create a Plotly Dash dashboard.

    Args:
        - app (flask.Flask): Flask application to be set as server of the Dash application.
    """
    with app.app_context():
        dash_app = dash.Dash(
            server=app,
            routes_pathname_prefix=DASH_APP_PREFIX,
            external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
        )
        app_setup(dash_app)
        app = dash_app.server


def app_setup(dash_app):
    """
    Will setup basic configuration for the Dash application, such as:
        - Base Layout
        - Route behaviour
        - Callbacks

    Args:
        - dash_app (dash.Dash): Dash application to setup.
    """
    dash_app.config.suppress_callback_exceptions = True
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

    register_line_graph_callbacks(dash_app)
    register_radar_callbacks(dash_app)

    @dash_app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')],
    )
    def display_page(pathname):
        """
        Resolves the content (layout) to be displayed based on the current path.

        Args:
            - pathname (str): Current endpoint of the dash application.

        Returns:
            - (html.Div | str): Resolved page content.
        """
        try:
            user = AuthHandler.handle_auth_request()
        except AuthHandlerException:
            return '403'

        if pathname == f'{DASH_APP_PREFIX}lines/':
            return get_lines_page_layout(user)
        if pathname == f'{DASH_APP_PREFIX}profile/':
            return get_profile_graph_layout(user)
        else:
            return '404'
