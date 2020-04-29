"""
Driving Profile graphs.
"""
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output

from app.database import DATABASE
from app.controllers.odb.session import SessionController

from app.plotly_dash.constants import Colors


def gen_radar_graph_figure(session_ids):
    session_controller = SessionController(user_id=1, db_session=DATABASE.session)
    sessions = session_controller.get_session_packages(session_ids)

    fig = go.Figure()
    colors = px.colors.sequential.tempo
    for idx, session in enumerate(sessions):
        df = pd.DataFrame(session)
        fig.add_trace(go.Scatterpolar(
            r=[
                max(df['engine_load'].values),
                max(df['engine_rpm'].values/100),
                max(df['fuel_level'].values),
                max(df['speed'].values),
            ],
            theta=['engine_load', 'engine_rpm', 'fuel_level', 'speed'],
            name=session['date'].strftime('%d/%m/%Y %H:%M'),
            line_color=colors[idx%len(colors)],
        ))

    fig.update_layout(template='plotly_dark')
    fig.update_traces(fill='toself')
    return fig


def get_profile_graph_layout(dash_app):
    session_controller = SessionController(user_id=1, db_session=DATABASE.session)
    session_options = [
        {'label': session.date.strftime('%d/%m/%Y %H:%M'), 'value': session.id}
        for session in session_controller.get_all(fields=['id', 'date'])
    ]

    layout = html.Div(
        style={'backgroundColor': Colors.BACKGROUND},
        children=[
            dcc.Dropdown(
                id='session-dropdown',
                options=session_options,
                value=[session_options[-1]['value']] if session_options else None,
                multi=True,
                style={
                    'color': Colors.BACKGROUND,
                    'padding': '0 1rem',
                    'margin-bottom': '1rem',
                },
            ),
            dcc.Graph(
                id='profile-graph',
                figure=gen_radar_graph_figure([]),
                style={'padding': '1rem'},
            )
        ],
    )

    @dash_app.callback(
        Output('profile-graph', 'figure'),
        [
            Input('session-dropdown', 'value'),
        ],
    )
    def update_profile_graph(session_ids):
        return gen_radar_graph_figure(session_ids)

    return layout
