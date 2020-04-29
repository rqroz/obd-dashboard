"""
Utility module for common functions/logic.
"""
import dash_html_components as html

from app.plotly_dash.constants import Colors


def get_default_label(text):
    return html.Label(
        text,
        style={
            'color': Colors.TEXT,
            'padding': '1rem',
        },
    )


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
