"""
Engine Views.
"""
from flask import jsonify

from app.controllers.odb.engine import EngineController
from app.decorators import auth_required


class EngineViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule(
            '/api/engine/load/average/',
            'engine_load_avg_view',
            view_func=cls.engine_load_avg_view,
            methods=('GET',),
        )
        server.add_url_rule(
            '/api/engine/rpm/average/',
            'engine_rpm_avg_view',
            view_func=cls.engine_rpm_avg_view,
            methods=('GET',),
        )

    @auth_required
    def engine_load_avg_view(user):
        """ Retrieves the average engine load for the current user """
        return jsonify({'average': EngineController().get_engine_load_avg(user)})

    @auth_required
    def engine_rpm_avg_view(user):
        """ Retrieves the average engine RPM for the current user """
        return jsonify({'average': EngineController().get_engine_rpm_avg(user)})
