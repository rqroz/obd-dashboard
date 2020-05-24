"""
GPS Views.
"""
from flask import jsonify

from app.controllers.odb.gps import GPSController
from app.decorators import auth_required


class GPSViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule(
            '/api/gps/',
            'gps_list_view',
            view_func=cls.gps_list_view,
            methods=('GET',),
        )
        server.add_url_rule(
            '/api/gps/latest/',
            'gps_latest_view',
            view_func=cls.gps_latest_view,
            methods=('GET',),
        )

    @auth_required
    def gps_list_view(user):
        """ Retrieves GPS locations registered for the current user """
        return jsonify({
            'trips': GPSController().get_gps_readings(user)
        })

    @auth_required
    def gps_latest_view(user):
        """ Retrieves the latest GPS coordinates for the current user """
        return jsonify({'trips': GPSController().get_sensor_latest_value(user)})
