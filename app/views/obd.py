"""
OBD-specific views.
"""
from structlog import get_logger
from flask import request

from app.controllers.obd import OBDController, OBDControllerError


LOGGER = get_logger(__name__)


class OBDViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule("/obd", "obd_view", view_func=cls.obd_view, methods=("GET",))

    def obd_view():
        """
        Receives TORQUE request and process the data accordingly.
        """
        controller = OBDController()
        try:
            controller.process_sensor_params(request.args)
        except OBDControllerError as err:
            LOGGER.error(str(err))

        return 'OK!'
