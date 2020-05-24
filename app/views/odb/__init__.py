"""
Base utility class for registering default sensor-related views.
"""
from flask import jsonify

from app.decorators import auth_required


class BaseSensorViews(object):
    SENSORS = [] # To be overriden by children
    VIEW_PREFIX = None # To be overriden by children
    CONTROLLER_CLASS = None # To be overriden by children

    @classmethod
    def _get_avg(cls, user, sensor_name):
        return jsonify({'average': cls.CONTROLLER_CLASS().get_sensor_avg(user, sensor_name)})

    @classmethod
    def _get_latest(cls, user, sensor_name):
        return jsonify({'value': cls.CONTROLLER_CLASS().get_sensor_latest_value(user, sensor_name)})

    @classmethod
    def add_views(cls, server):
        for sensor_name in cls.SENSORS:
            avg_view_func_name = f'{sensor_name}_avg_view'
            avg_view_name = f'engine_{avg_view_func_name}'
            server.add_url_rule(
                f'/api/{cls.VIEW_PREFIX}/{sensor_name}/average/',
                avg_view_name,
                view_func=getattr(cls, avg_view_func_name),
                methods=('GET',),
            )

            latest_view_func_name = f'{sensor_name}_latest_view'
            latest_view_name = f'engine_{latest_view_func_name}'
            server.add_url_rule(
                f'/api/{cls.VIEW_PREFIX}/{sensor_name}/latest/',
                latest_view_name,
                view_func=getattr(cls, latest_view_func_name),
                methods=('GET',),
            )
