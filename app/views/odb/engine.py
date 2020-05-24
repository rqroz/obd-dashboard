"""
Engine Views.
"""
from flask import jsonify

from app.constants.odb import BatteryLevel
from app.controllers.odb.engine import EngineController
from app.decorators import auth_required


class EngineViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule(
            '/api/engine/load/average/',
            'engine_load_avg_view',
            view_func=cls.load_avg_view,
            methods=('GET',),
        )
        server.add_url_rule(
            '/api/engine/rpm/average/',
            'engine_rpm_avg_view',
            view_func=cls.rpm_avg_view,
            methods=('GET',),
        )
        server.add_url_rule(
            '/api/engine/battery/latest/',
            'battery_latest_read_view',
            view_func=cls.battery_latest_read_view,
            methods=('GET',),
        )

    @auth_required
    def load_avg_view(user):
        """ Retrieves the average engine load for the current user """
        return jsonify({'average': EngineController().get_load_avg(user)})

    @auth_required
    def rpm_avg_view(user):
        """ Retrieves the average engine RPM for the current user """
        return jsonify({'average': EngineController().get_rpm_avg(user)})

    @auth_required
    def battery_latest_read_view(user):
        last_battery_read = EngineController().get_battery_latest_read(user)

        message = None
        if last_battery_read < BatteryLevel.MIN:
            message = 'Your battery\'s voltage is under the minimum recommended. Please change the battery soon.'

        return jsonify({
            'value': last_battery_read,
            'message': message,
        })
