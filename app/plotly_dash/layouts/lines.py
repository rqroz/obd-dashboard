"""
Module for the line graph layout.
"""
import dash_html_components as html
import dash_core_components as dcc

from app.plotly_dash.callbacks.lines import gen_line_graph_figure
from app.plotly_dash.constants import Colors, CHART_TYPES
from app.plotly_dash.utils import get_default_label, get_session_dropdown_options


def get_lines_page_layout(user):
    """
    Creates the layout for the line graph page content.

    Args:
        - user (app.models.user.User): Current user from request.

    Returns:
        - (html.Div): The page layout containing two dropdowns and a dynamic line graph.
    """
    session_options = get_session_dropdown_options(user)
    layout = html.Div(
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

    return layout
