"""
Constants specific to the Plotly Dash app.
"""
class Colors:
    BACKGROUND = '#1E1E1E'
    TEXT = '#FFF'


CHART_TYPES = [
    {'label': 'Battery Voltage (V)', 'value': 'engine_voltage_readings'},
    {'label': 'Commanded Equivalence Ratio (lambda)', 'value': 'fuel_lambda_readings'},
    {'label': 'Engine Load (%)', 'value': 'engine_load_readings'},
    {'label': 'Engine Coolant Temperature (°C)', 'value': 'engine_coolant_temp_readings'},
    {'label': 'Fuel Level (%)', 'value': 'fuel_level_readings'},
    {'label': 'Fuel Ratio (Km/L)', 'value': 'fuel_ratio_readings'},
    {'label': 'Manifold Pressure (kPa)', 'value': 'engine_map_readings'},
    {'label': 'Mass Air Flow Rate (g/s)', 'value': 'engine_maf_readings'},
    {'label': 'RPM', 'value': 'engine_rpm_readings'},
    {'label': 'Speed (Km/h)', 'value': 'speed_readings'},
]


CHART_TYPE_MAP = {type['value']: type['label'] for type in CHART_TYPES}


DASH_APP_PREFIX = '/dash/'
