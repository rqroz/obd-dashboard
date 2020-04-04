"""
Auth Views
"""
from flask import jsonify, request
from structlog import get_logger

from app.config import Config
from app.controllers.auth import AuthController, AuthControllerException
from app.decorators import auth_required


LOGGER = get_logger(__name__)


class AuthViews:
    @classmethod
    def add_views(cls, server):
        server.add_url_rule('/api/login/', view_func=cls.login_view, methods=('POST',))
        server.add_url_rule('/api/logout/', view_func=cls.logout_view, methods=('POST',))

    def login_view():
        controller = AuthController()
        try:
            user = controller.login(request.get_json())
        except AuthControllerException as exc:
            response = jsonify({'message': 'Login Failed', 'errors': exc.errors})
            response.status_code = 400
            return response

        auth_token = controller.get_token(user)

        response = jsonify({
            'message': 'Login successful',
            'user': user.to_dict(include_protected=True),
        })
        response.set_cookie(Config.AUTH_TOKEN_NAME, auth_token)
        return response

    @auth_required
    def logout_view(_):
        response = jsonify({'message': 'Successfully logged out'})
        response.delete_cookie(Config.AUTH_TOKEN_NAME)
        return response
