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


class SessionController(BaseUserController):
    """
    Controller class for ODB Session data manipulations.
    """
    def _resolve_query(self, fields: List[str]):
        """
        Will resolve the query arguments (projection) based on <fields>.

        Args:
            - fields (List[str]): Name of session attributes to project.

        Returns:
            - (List[str] | List[app.models.odb.session.ODBSession]): Resulting query.
        """
        return (
            [getattr(ODBSession, key) for key in fields]
            if fields and isinstance(fields, list)
            else [ODBSession]
        )

    def get(self, id: int, fields: List[str] = None):
        """
        Returns an ODBSession instance based on its id and the current user.

        Args:
            - id (int): Id of the target ODBSession.
            - fields (List[str]): List of fields to project.

        Returns:
            - (app.models.odb.session.ODBSession | None): An ODBSession instance, if any is found. None otherwise.
        """
        return (
            self.db_session.query(*self._resolve_query(fields))
                            .filter(
                                ODBSession.id == id,
                                ODBSession.user_id == self.user_id,
                            )
                            .first()
        )

    def get_all(self, fields: List[str] = None):
        """
        Returns all of the ODBSession records for the current user.

        Args:
            - fields (List[str]): List of fields to project.

        Returns:
            - (List[app.models.odb.session.ODBSession]): List of records found.
        """
        if not self.user_id:
            return []

        return (
            self.db_session.query(*self._resolve_query(fields))
                            .filter(ODBSession.user_id == self.user_id)
        )

    def get_or_create(self, id: int):
        """
        Will look for an ODBSession record within the database based on <id> and the current user.
        If the record is not found, will create one and return it.

        Args:
            - id (int): Id of the target ODBSession.

        Returns:
            - session (app.models.odb.session.ODBSession): Resulting instance of ODBSession.
        """
        session = self.get(id)
        if not session:
            session = ODBSession(user_id=self.user_id, id=id)
            self.db_session.add(session)
            self.db_session.commit()

        return session

    def get_session_packages(self, ids: int):
        """
        Will retrieve a list of ODBSession from the database and include in the query the following items:
            - engine_load_readings
            - engine_rpm_readings
            - fuel_level_readings
            - speed_readings

        Then, will create a list of packages to be fed to the graphs containing data from the session
        and a summarized list of values for each of the items loaded.

        Args:
            - ids (int): List of ODBSession ids to look for.

        Returns:
            - (List[dict]): Data package to feed graphs.
        """
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
                            .options(selectinload(ODBSession.fuel_ratio_readings))
                            .options(selectinload(ODBSession.speed_readings))
        )

        data = []
        for session in sessions:
            sesh = session.to_dict()
            sesh['engine_load'] = [r.value for r in session.engine_load_readings]
            sesh['engine_rpm'] = [r.value for r in session.engine_rpm_readings]
            sesh['fuel_level'] = [r.value for r in session.fuel_level_readings]
            sesh['fuel_ratio'] = [r.value for r in session.fuel_ratio_readings]
            sesh['speed'] = [r.value for r in session.speed_readings]
            data.append(sesh)

        return data
