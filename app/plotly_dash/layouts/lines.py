"""
Line graphs for multiple sensors.
"""
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output

from app.database import DATABASE
from app.controllers.odb.session import SessionController

from app.plotly_dash.constants import (
    Colors,
    CHART_TYPES,
    CHART_TYPE_MAP,
)
from app.plotly_dash.utils import get_default_label


def gen_line_graph_figure(items):
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
        yaxis={'title': 'Speed (km/h)'},
        legend={'x': 0, 'y': 1},
        hovermode='closest',
        plot_bgcolor=Colors.BACKGROUND,
        paper_bgcolor=Colors.BACKGROUND,
        font={'color': Colors.TEXT},
    )
    return dict(layout=layout, data=data)


def get_lines_page_layout(dash_app):
    session_controller = SessionController(user_id=1, db_session=DATABASE.session)
    session_options = [
        {'label': session.date.strftime('%d/%m/%Y %H:%M'), 'value': session.id}
        for session in session_controller.get_all(fields=['id', 'date'])
    ]

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

    @dash_app.callback(
        Output('line-graph', 'figure'),
        [
            Input('session-dropdown', 'value'),
            Input('chart-type-dropdown', 'value'),
        ],
    )
    def update_lines_graph(session_id, selected_attrs):
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

    return layout
