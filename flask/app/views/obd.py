"""
OBD-specific views.
"""
from flask import jsonify, request


class OBDViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule("/obd", "obd_view", view_func=cls.obd_view, methods=("GET",))

    def obd_view():
        return 'OK!'
