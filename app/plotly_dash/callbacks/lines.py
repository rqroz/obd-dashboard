"""
Module for line graph callbacks.
"""
import pandas as pd

from dash.dependencies import Input, Output
from typing import List

from app.plotly_dash.constants import Colors, CHART_TYPE_MAP
from app.plotly_dash.utils import get_session_controller


def gen_line_graph_figure(items: List[dict]):
    """
    Generates the figure for the line graph.

    Args:
        - items (List[dict]): List of items containing a dataframe (mapped on 'df' key) and a title.

    Returns:
        - (dict): Figure map containing layout and data.
    """
    data = [
        dict(
            x=item['df']['x'],
            y=item['df']['y'],
            text=item['df']['date'],
            mode='line',
            opacity=0.7,
            marker={
                'size': 5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=item['title']
        ) for item in items
    ]
    layout = dict(
        xaxis={'title': 'Index'},
        yaxis={'title': 'Value'},
        legend={'x': 0, 'y': 1},
        hovermode='closest',
        plot_bgcolor=Colors.BACKGROUND,
        paper_bgcolor=Colors.BACKGROUND,
        font={'color': Colors.TEXT},
    )
    return dict(layout=layout, data=data)


def register_line_graph_callbacks(dash_app):
    """
    Register callbacks for the line graph.

    Args:
        - dash_app (dash.Dash): Dash application.
    """
    @dash_app.callback(
        Output('line-graph', 'figure'),
        [
            Input('session-dropdown', 'value'),
            Input('chart-type-dropdown', 'value'),
        ],
    )
    def update_lines_graph(session_id: int, selected_attrs: List[str]):
        """
        Callback for when either the session or the selected attributes are changed.

        Raises:
            - AuthHandlerException: if request is not authenticated.

        Args:
            - session_id (int): Selected session id.
            - selected_attrs (List[str]): List of sensors to be considered.

        Returns:
            - (dict): Generated line graph figure.
        """
        session = get_session_controller().get(session_id).to_flat_data()
        car_states = session['car_states']
        indexes = [idx for idx, _ in enumerate(car_states)]

        items = []
        if session:
            for attr in selected_attrs:
                item = {
                    'df': pd.DataFrame({
                        'x': indexes,
                        'y': [state[attr] for state in car_states],
                        'date': [state['date'] for state in car_states],
                    }),
                    'title': CHART_TYPE_MAP[attr],
                }
                items.append(item)

        return gen_line_graph_figure(items)
