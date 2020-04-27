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
            '/api/obd/upload/',
            'obd_csv_upload',
            view_func=cls.obd_csv_upload,
            methods=('POST',)
        )
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
        return jsonify({'trips': OBDController().get_gps_readings(user)})

    @auth_required
    def obd_csv_upload(user):
        """ Registers sensor information through a CSV file sent by the client """
        try:
            csv_file = request.files['file']
        except KeyError:
            response = jsonify({'message': 'Missing CSV file'})
            response.status_code = 400
            return response

        controller = OBDController()
        try:
            controller.process_csv(user, csv_file)
        except OBDControllerError as err:
            message = str(err)
            LOGGER.error('Unable to process CSV file', error=message)
            response = jsonify({'message': message})
            response.status_code = 400
            return response

        return jsonify({'message': 'Successfully processed the file'})
