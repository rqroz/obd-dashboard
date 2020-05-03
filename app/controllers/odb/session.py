"""
ODB Controller
"""
from typing import List
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func

from app.controllers import BaseUserController
from app.models.odb.session import ODBSession
from app.models.odb.engine import EngineLoad
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
                            .filter(
                                ODBSession.id == id,
                                ODBSession.user_id == self.user_id,
                            )
                            .first()
        )

    def get_all(self, fields: List[str] = None):
        if not self.user_id:
            return []

        return (
            self.db_session.query(*self._resolve_query(fields))
                            .filter(ODBSession.user_id == self.user_id)
        )

    def get_session_packages(self, ids: int):
        if not self.user_id:
            return {}

        sessions = (
            self.db_session.query(ODBSession)
                            .filter(
                                ODBSession.user_id == self.user_id,
                                ODBSession.id.in_(ids),
                            )
                            .options(selectinload(ODBSession.engine_load_readings))
                            .options(selectinload(ODBSession.engine_rpm_readings))
                            .options(selectinload(ODBSession.fuel_level_readings))
                            .options(selectinload(ODBSession.speed_readings))
        )

        def process_list(readings):
            reading_values = [r.value for r in readings]
            max_value = max(reading_values)
            return [val/max_value for val in reading_values]

        data = []
        for session in sessions:
            sesh = session.to_dict()
            sesh['engine_load'] = [r.value for r in session.engine_load_readings]
            sesh['engine_rpm'] = [r.value for r in session.engine_rpm_readings]
            sesh['fuel_level'] = [r.value for r in session.fuel_level_readings]
            sesh['speed'] = [r.value for r in session.speed_readings]
            data.append(sesh)

        return data
