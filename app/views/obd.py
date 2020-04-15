"""
OBD Views.
"""
from structlog import get_logger
from flask import request, jsonify

from app.controllers.obd import OBDController, OBDControllerError
from app.decorators import auth_required


LOGGER = get_logger(__name__)


class OBDViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule('/obd', 'obd_view', view_func=cls.obd_view, methods=('GET',))
        server.add_url_rule(
            '/api/locations/',
            'location_list_view',
            view_func=cls.location_list_view,
            methods=('GET',),
        )

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

    @auth_required
    def location_list_view(user):
        """ Retrieves GPS locations registered for the current user """
        return jsonify({'locations': OBDController().get_gps_readings(user)})
