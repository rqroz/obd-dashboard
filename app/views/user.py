"""
User Views
"""
from flask import jsonify, request
from structlog import get_logger

from app.config import Config
from app.controllers.user import UserController, UserControllerException
from app.controllers.auth import AuthController
from app.decorators import auth_required


LOGGER = get_logger(__name__)


class UserViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule('/api/register/', view_func=cls.registration_view, methods=('POST',))
        server.add_url_rule('/api/profile/', view_func=cls.profile_view, methods=('GET',))

    def registration_view():
        """ Registers a new user """
        user_controller = UserController()
        try:
            user = user_controller.create_user(request.get_json())
        except UserControllerException as exc:
            LOGGER.error('Could not register new user', **exc.errors)
            response = jsonify({'message': 'Registration Failed', 'errors': exc.errors})
            response.status_code = 400
            return response

        auth_token = AuthController().get_token(user).decode('utf-8')

        response = jsonify({
            'message': 'Registration successful',
            'user': user.to_dict(include_protected=True, replace_id=True),
        })
        response.set_cookie(Config.AUTH_TOKEN_NAME, auth_token)
        return response

    @auth_required
    def profile_view(user_id):
        controller = UserController(user_id=user_id)
        return jsonify({'user': controller.get_user().to_dict(include_protected=True, replace_id=True)})
