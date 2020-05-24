"""
Fuel Views.
"""
from flask import jsonify

from app.controllers.odb.fuel import FuelController
from app.decorators import auth_required


class FuelViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule(
            '/api/fuel/level/latest/',
            'latest_fuel_level',
            view_func=cls.latest_fuel_level,
            methods=('GET',),
        )

    @auth_required
    def latest_fuel_level(user):
        """ Retrieves the latest fuel level for the current user """
        return jsonify({'level': FuelController().get_latest_fuel_level(user)})
