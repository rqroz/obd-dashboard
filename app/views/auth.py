"""
Auth Views
"""
from flask import jsonify, request
from structlog import get_logger

from app.controllers.auth import AuthController, AuthControllerException


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

        return jsonify({'message': 'Login successful', 'user': user.to_dict(include_protected=True)})

    def logout_view():
        return jsonify({'message': 'Successfully logged out'})
