"""
Base data manipulation classes.
"""
from flask import g


class BaseController(object):
    """
    Base data controller.

    Attributes:
        - db_session (flask_sqlalchemy.SQLAlchemy.session): Database session instance.
    """
    def __init__(self, db_session=None):
        """ Class Constructor """
        if db_session is None:
            db_session = g.db_session
        self.db_session = db_session


class BaseUserController(BaseController):
    """
    Base controller for user related data.

    Attributes:
        - db_session (flask_sqlalchemy.SQLAlchemy.session): Database session instance.
        - user_id (int): Id of the current user, if any.
    """
    def __init__(self, user_id=None, db_session=None):
        super(BaseUserController, self).__init__(db_session)
        self.user_id = user_id
