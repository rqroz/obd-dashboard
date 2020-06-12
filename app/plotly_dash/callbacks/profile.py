"""
Module for driving profile graph callbacks.
"""
import plotly.express as px
import plotly.graph_objects as go

from decimal import Decimal
from typing import List
from dash.dependencies import Input, Output

from app.plotly_dash.utils import get_session_controller


def get_polar_value(sequence: List[Decimal]):
    """
    Will process <sequence> to get the resulting value for the profile graph.

    Args:
        - sequence (List[Decimal]): List of sensor values.

    Returns:
        - (float): Normalized average.
    """
    sequence_length = len(sequence)
    if not sequence_length:
        return 0

    max_val = max(sequence)
    if max_val == 0:
        return 0

    return sum([val/max_val for val in sequence])/sequence_length


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
        fig.add_trace(
            go.Scatterpolar(
                r=[
                    get_polar_value(session['engine_load']),
                    get_polar_value(session['engine_rpm']),
                    get_polar_value(session['engine_maf']),
                    get_polar_value(session['engine_map']),
                    get_polar_value(session['engine_coolant_temp']),
                    get_polar_value(session['fuel_ratio']),
                    get_polar_value(session['fuel_lambda']),
                    get_polar_value(session['speed']),
                ],
                theta=[
                    'Engine Load',
                    'Engine RPM',
                    'Mass Air Flow',
                    'Manifold Pressure',
                    'Engine Coolant Temperature',
                    'Fuel Ratio',
                    'Commanded Equivalence Ratio (lambda)',
                    'Speed',
                ],
                name=session['date'].strftime('%d/%m/%Y %H:%M'),
                line_color=colors[idx%len(colors)],
            )
        )

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
