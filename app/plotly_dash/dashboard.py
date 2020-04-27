"""
Dash App Module.
"""
import dash
import dash_html_components as html
import dash_core_components as dcc

from flask import Flask


def init_plotly_dash(app: Flask):
    """ Create a Plotly Dash dashboard. """
    with app.app_context():
        dash_app = dash.Dash(
            server=app,
            routes_pathname_prefix='/dash/',
        )

        create_layout(dash_app)
        init_callbacks(dash_app)
        app = dash_app.server


def create_layout(dash_app):
    dash_app.layout = html.Div(children=[
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])


def init_callbacks(dash_app):
    pass
