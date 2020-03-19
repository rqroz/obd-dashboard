"""
OBD-specific views.
"""
from structlog import get_logger
from flask import jsonify, request


logger = get_logger(__name__)


class OBDViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule("/obd", "obd_view", view_func=cls.obd_view, methods=("GET",))

    def obd_view():
        logger.info('OBD Request received')
        return 'OK!'
