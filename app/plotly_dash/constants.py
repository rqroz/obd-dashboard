"""
Constants specific to the Plotly Dash app.
"""
class Colors:
    BACKGROUND = '#1E1E1E'
    TEXT = '#FFF'


CHART_TYPES = [
    {'label': 'Battery Voltage (V)', 'value': 'voltage'},
    {'label': 'Commanded Equivalence Ratio (lambda)', 'value': 'fuel_cmd_equivalence_ratio'},
    {'label': 'Engine Load (%)', 'value': 'engine_load'},
    {'label': 'Engine Coolant Temperature (°C)', 'value': 'engine_coolant_temp'},
    {'label': 'Fuel Level (%)', 'value': 'fuel_level'},
    {'label': 'Fuel Ratio (Km/L)', 'value': 'fuel_ratio'},
    {'label': 'Manifold Pressure (kPa)', 'value': 'engine_map'},
    {'label': 'Mass Air Flow Rate (g/s)', 'value': 'engine_maf'},
    {'label': 'RPM', 'value': 'engine_rpm'},
    {'label': 'Speed (Km/h)', 'value': 'speed'},
]


CHART_TYPE_MAP = {type['value']: type['label'] for type in CHART_TYPES}


DASH_APP_PREFIX = '/dash/'
