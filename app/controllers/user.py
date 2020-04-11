"""
User Controller
"""
import uuid

from bcrypt import gensalt, hashpw
from flask import g
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from structlog import get_logger
from typing import List

from app.controllers import BaseUserController
from app.models.user import User
from app.validators.user import UserCreateSchema
from app.utils.exceptions import DictException


LOGGER = get_logger(__name__)


class UserControllerException(DictException):
    """ Exception class for UserController class """
    pass


class UserController(BaseUserController):
    """
    Controller class for user related data manipulations.
    """
    def create_user(self, data):
        """
        Creates a new user record in the database.

        Raises:
            - UserControllerError: if validation fails;
                                   if is unable to save the new record into the database due to an integrity error.

        Args:
            - data (dict): Map of user data to be validated and further processed as a User instance.

        Returns:
            - user (app.models.user.User): User instance created from <data>.
        """
        validator = UserCreateSchema()
        try:
            loaded_data = validator.load(data)
        except ValidationError as error:
            raise UserControllerException(error.messages)

        loaded_data['password'] = hashpw(loaded_data['password'].encode('utf8'), gensalt())
        loaded_data.pop('confirm_password')
        user = User(public_id=str(uuid.uuid4()), **loaded_data)

        self.db_session.add(user)
        try:
            self.db_session.commit()
        except IntegrityError as err:
            raise UserControllerException({'forbidden': 'User with that email already exists'})

        self.user_id = user.id
        return user

    def get_user(self, **kwargs):
        """
        Gets a user from DB.
        Will fetch the first item matching keyword arguments informed.

        Returns:
            (app.models.user.User | None): First item matching kwargs, if any. None otherwise.
        """
        if not self.user_id:
            return (
                self.db_session.query(User)
                                .filter(*[getattr(User, key) == value for key, value in kwargs.items()])
                                .first()
            )

        return self.db_session.query(User).filter(User.id == self.user_id).first()
