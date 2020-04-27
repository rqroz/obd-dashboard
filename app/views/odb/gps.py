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
            '/api/gps/locations/',
            'location_list_view',
            view_func=cls.location_list_view,
            methods=('GET',),
        )

    @auth_required
    def location_list_view(user):
        """ Retrieves GPS locations registered for the current user """
        return jsonify({'trips': GPSController().get_gps_readings(user)})
