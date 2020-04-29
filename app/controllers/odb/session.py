"""
ODB Controller
"""
from typing import List
from sqlalchemy.orm import selectinload

from app.controllers import BaseUserController
from app.models.odb.session import ODBSession
from app.models.user import User


class SessionControllerError(Exception):
    """ Exception class for SessionController """
    pass


class SessionController(BaseUserController):
    """
    Controller class for ODB Session data manipulations.
    """
    def _resolve_query(self, fields):
        return (
            [getattr(ODBSession, key) for key in fields]
            if fields and isinstance(fields, list)
            else [ODBSession]
        )

    def get(self, id: int, fields: List[str] = None):
        return (
            self.db_session.query(*self._resolve_query(fields))
                            .filter(ODBSession.id == id)
                            .first()
        )

    def get_all(self, fields: List[str] = None):
        if not self.user_id:
            return []

        return (
            self.db_session.query(*self._resolve_query(fields))
                            .filter(ODBSession.user_id == self.user_id)
        )
