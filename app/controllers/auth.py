"""
Authentication controller
"""
import jwt
import datetime

from bcrypt import checkpw, gensalt, hashpw
from marshmallow import ValidationError

from app.config import Config
from app.controllers import BaseUserController
from app.controllers.user import UserController
from app.utils.exceptions import DictException
from app.validators.auth import LoginSchema


class AuthControllerException(DictException):
    """ Exception class for AuthController class """
    pass


class AuthController(object):
    """
    Controller for authentication related data.
    """
    def login(self, data):
        validator = LoginSchema()
        try:
            loaded_data = validator.load(data)
        except ValidationError as error:
            raise AuthControllerException(error.messages)

        user: User = UserController().get_user(email=loaded_data['email'])
        try:
            assert checkpw(loaded_data['password'].encode('utf8'), user.password)
        except (AssertionError, AttributeError):
            raise AuthControllerException({'invalid': 'Incorrect user and/or password'})

        return user

    def get_token(self, user):
        return jwt.encode(
            {
                'public_id': user.public_id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            Config.SECRET_KEY,
        )
