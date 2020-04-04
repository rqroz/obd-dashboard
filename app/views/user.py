"""
User Views
"""
from flask import jsonify, request
from structlog import get_logger

from app.controllers.user import UserController, UserControllerException


LOGGER = get_logger(__name__)


class UserViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule('/api/register/', view_func=cls.registration_view, methods=('POST',))

    def registration_view():
        """ Registers a new user """
        controller = UserController()
        try:
            user = controller.create_user(request.get_json())
        except UserControllerException as exc:
            LOGGER.error('Could not register new user', **exc.errors)
            response = jsonify({'message': 'Registration Failed', 'errors': exc.errors})
            response.status_code = 400
            return response

        return jsonify({'message': 'Registration successful', 'user': user.to_dict(include_protected=True)})
