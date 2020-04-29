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
