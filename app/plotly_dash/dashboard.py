"""
Dash App Module.
"""
import pandas as pd

import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from flask import Flask

from app.plotly_dash.constants import (
    Colors,
    CHART_TYPES,
    CHART_TYPE_MAP,
)
from app.plotly_dash.utils import (
    get_default_label,
    gen_line_graph_figure,
)

from app.database import DATABASE
from app.controllers.odb.session import SessionController


def init_plotly_dash(app: Flask):
    """ Create a Plotly Dash dashboard. """
    with app.app_context():
        dash_app = dash.Dash(
            server=app,
            routes_pathname_prefix='/dash/',
            external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
        )

        create_layout(dash_app)
        init_callbacks(dash_app)
        app = dash_app.server


def create_layout(dash_app):
    session_controller = SessionController(user_id=1, db_session=DATABASE.session)
    session_options = [
        {'label': session.date.strftime('%d/%m/%Y %H:%M'), 'value': session.id}
        for session in session_controller.get_all(fields=['id', 'date'])
    ]

    dash_app.layout = html.Div(
        style={'backgroundColor': Colors.BACKGROUND},
        children=[
            get_default_label('Session'),
            dcc.Dropdown(
                id='session-dropdown',
                options=session_options,
                value=session_options[-1]['value'] if session_options else None,
                style={
                    'color': Colors.BACKGROUND,
                    'padding': '0 1rem',
                    'margin-bottom': '1rem',
                },
            ),
            get_default_label('Sensor'),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=CHART_TYPES if session_options else [],
                value=[],
                multi=True,
                style={
                    'color': Colors.BACKGROUND,
                    'padding': '0 1rem',
                },
            ),
            dcc.Graph(
                id='line-graph',
                figure=gen_line_graph_figure([]),
                style={'padding-top': '1rem'},
            )
        ],
    )


def init_callbacks(dash_app):
    @dash_app.callback(
        Output('line-graph', 'figure'),
        [
            Input('session-dropdown', 'value'),
            Input('chart-type-dropdown', 'value'),
        ],
    )
    def update_graph(session_id, selected_attrs):
        session_controller = SessionController(user_id=1, db_session=DATABASE.session)
        session = session_controller.get(session_id)

        items = []
        if session:
            for attr in selected_attrs:
                readings = getattr(session, attr)
                item = {
                    'df': pd.DataFrame({
                        'x': [idx for idx, _ in enumerate(readings)],
                        'y': [r.value for r in readings],
                        'date': [r.date for r in readings],
                    }),
                    'title': CHART_TYPE_MAP[attr],
                }
                items.append(item)

        return gen_line_graph_figure(items)
