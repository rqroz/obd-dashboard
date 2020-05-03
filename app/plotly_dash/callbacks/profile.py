"""
Module for driving profile graph callbacks.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from typing import List
from dash.dependencies import Input, Output

from app.plotly_dash.utils import get_session_controller


def gen_radar_graph_figure(session_ids: List[int]):
    """
    Generates the figure for the radar plot based on <session_ids>.

    Args:
        - session_ids (List[int]): List of session ids to be considered.
    """
    sessions = get_session_controller().get_session_packages(session_ids or [])

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


def register_radar_callbacks(dash_app):
    """
    Will register all the callbacks for the profile section.

    Raises:
        - AuthHandlerException: if request is not authenticated.

    Args:
        - dash_app (dash.Dash): Current dash application.
    """
    @dash_app.callback(
        Output('profile-graph', 'figure'),
        [
            Input('session-dropdown', 'value'),
        ],
    )
    def update_profile_graph(session_ids: List[int]):
        """
        Callback for when user changes the list of sessions to be considered for profiling.

        Args:
            - session_ids (List[int]): List of session ids to be considered.

        Returns:
            - (dict): Generated radar plot figure.
        """
        return gen_radar_graph_figure(session_ids)
