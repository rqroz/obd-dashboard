"""
Module for the driving profile graph layout.
"""
import dash_html_components as html
import dash_core_components as dcc

from app.plotly_dash.callbacks.profile import gen_radar_graph_figure
from app.plotly_dash.constants import Colors
from app.plotly_dash.utils import get_session_dropdown_options


def get_profile_graph_layout(user):
    """
    Creates the layout for the profile graph page content.

    Args:
        - user (app.models.user.User): Current user from request.

    Returns:
        - (html.Div): The page layout with a session dropdown and a dynamic radar plot.
    """
    session_options = get_session_dropdown_options(user)
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

    return layout
