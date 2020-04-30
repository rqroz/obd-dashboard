import jwt

from flask import g, request, jsonify

from app.config import Config
from app.models.user import User


class AuthHandlerException(Exception):
    """ Exception class for authentication handlers """
    pass


class AuthHandler:
    @staticmethod
    def handle_auth_request():
        auth_token = request.cookies.get(Config.AUTH_TOKEN_NAME)
        if not auth_token:
            raise AuthHandlerException

        try:
            token_info = jwt.decode(auth_token, Config.SECRET_KEY)
        except:
            raise AuthHandlerException

        user = g.db_session.query(User).filter(User.public_id == token_info['public_id']).first()
        if not user:
            raise AuthHandlerException

        return user

    @staticmethod
    def get_unauth_response():
        response = jsonify({'message': 'Unauthorized'})
        response.status_code = 401
        return response
