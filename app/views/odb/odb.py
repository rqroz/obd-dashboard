"""
ODB Views.
"""
from structlog import get_logger
from flask import request, jsonify

from app.controllers.odb.odb import ODBController, ODBControllerError
from app.decorators import auth_required


LOGGER = get_logger(__name__)


class ODBViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule('/obd', 'obd_view', view_func=cls.obd_view, methods=('GET',))
        server.add_url_rule(
            '/api/obd/upload/',
            'obd_csv_upload',
            view_func=cls.obd_csv_upload,
            methods=('POST',)
        )

    def obd_view():
        """
        Receives TORQUE request and process the data accordingly.
        """
        controller = ODBController()
        try:
            controller.process_sensor_params(request.args)
        except ODBControllerError as err:
            LOGGER.error(str(err))

        return 'OK!'

    @auth_required
    def obd_csv_upload(user):
        """ Registers sensor information through a CSV file sent by the client """
        try:
            csv_file = request.files['file']
        except KeyError:
            response = jsonify({'message': 'Missing CSV file'})
            response.status_code = 400
            return response

        controller = ODBController()
        try:
            controller.process_csv(user, csv_file)
        except ODBControllerError as err:
            message = str(err)
            LOGGER.error('Unable to process CSV file', error=message)
            response = jsonify({'message': message})
            response.status_code = 400
            return response

        return jsonify({'message': 'Successfully processed the file'})
