import jwt

from functools import wraps
from flask import g, request, jsonify

from app.config import Config
from app.models.user import User


def default_unauth_response():
    response = jsonify({'message': 'Unauthorized'})
    response.status_code = 401
    return response


def auth_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        auth_token = request.cookies.get(Config.AUTH_TOKEN_NAME)
        if not auth_token:
            return default_unauth_response()

        try:
            token_info = jwt.decode(auth_token, Config.SECRET_KEY)
        except:
            return default_unauth_response()

        user = g.db_session.query(User).filter(User.public_id == token_info['public_id']).first()
        if not user:
            return default_unauth_response()

        return func(user, *args, **kwargs)

    return decorator
