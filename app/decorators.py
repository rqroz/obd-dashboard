from functools import wraps

from app.utils.auth import AuthHandler, AuthHandlerException


def auth_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            user = AuthHandler.handle_auth_request()
        except AuthHandlerException:
            return AuthHandler.get_unauth_response()

        return func(user, *args, **kwargs)

    return decorator
