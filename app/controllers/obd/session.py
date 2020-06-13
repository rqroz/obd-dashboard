"""
Session Controller
"""
from typing import List
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func

from app.constants.obd import BatteryLevel
from app.controllers import BaseUserController
from app.models.obd.car import CarState, Engine
from app.models.obd.session import OBDSession
from app.models.user import User


class SessionController(BaseUserController):
    """
    Controller class for OBD Session data manipulations.
    """
    def _resolve_query(self, fields: List[str]):
        """
        Will resolve the query arguments (projection) based on <fields>.

        Args:
            - fields (List[str]): Name of session attributes to project.

        Returns:
            - (List[str] | List[app.models.obd.session.OBDSession]): Resulting query.
        """
        return (
            [getattr(OBDSession, key) for key in fields]
            if fields and isinstance(fields, list)
            else [OBDSession]
        )

    def get(self, id: int, fields: List[str] = None):
        """
        Returns an OBDSession instance based on its id and the current user.

        Args:
            - id (int): Id of the target OBDSession.
            - fields (List[str]): List of fields to project.

        Returns:
            - (app.models.obd.session.OBDSession | None): An OBDSession instance, if any is found. None otherwise.
        """
        return (
            self.db_session.query(*self._resolve_query(fields))
                            .filter(
                                OBDSession.id == id,
                                OBDSession.user_id == self.user_id,
                            )
                            .first()
        )

    def get_all(self, fields: List[str] = None):
        """
        Returns all of the OBDSession records for the current user.

        Args:
            - fields (List[str]): List of fields to project.

        Returns:
            - (List[app.models.obd.session.OBDSession]): List of records found.
        """
        if not self.user_id:
            return []

        return (
            self.db_session.query(*self._resolve_query(fields))
                            .filter(OBDSession.user_id == self.user_id)
        )

    def get_or_create(self, id: int):
        """
        Will look for an OBDSession record within the database based on <id> and the current user.
        If the record is not found, will create one and return it.

        Args:
            - id (int): Id of the target OBDSession.

        Returns:
            - session (app.models.obd.session.OBDSession): Resulting instance of OBDSession.
        """
        session = self.get(id)
        if not session:
            session = OBDSession(user_id=self.user_id, id=id)
            self.db_session.add(session)
            self.db_session.commit()

        return session

    def get_session_packages(self, ids: int):
        """
        Will retrieve a list of OBDSession from the database and include in the query the following items:
            - engine_load_readings
            - engine_rpm_readings
            - fuel_level_readings
            - speed_readings

        Then, will create a list of packages to be fed to the graphs containing data from the session
        and a summarized list of values for each of the items loaded.

        Args:
            - ids (int): List of OBDSession ids to look for.

        Returns:
            - (List[dict]): Data package to feed graphs.
        """
        if not self.user_id:
            return {}

        sessions = (
            self.db_session.query(OBDSession)
                            .filter(
                                OBDSession.user_id == self.user_id,
                                OBDSession.id.in_(ids),
                            )
                            .options(selectinload(OBDSession.car_states))
        )

        data = []
        for session in sessions:
            sesh = session.to_dict()
            list_keys = [
                'engine_load', 'engine_rpm', 'engine_maf', 'engine_map',
                'engine_coolant_temp', 'fuel_ratio', 'fuel_lambda', 'speed',
            ]
            for key in list_keys:
                sesh[key] = []

            for state in session.car_states:
                sesh['engine_load'].append(state.engine.load)
                sesh['engine_rpm'].append(state.engine.rpm)
                sesh['engine_maf'].append(state.engine.maf)
                sesh['engine_map'].append(state.engine.map)
                sesh['engine_coolant_temp'].append(state.engine.coolant_temp)
                sesh['fuel_ratio'].append(state.fuel.ratio)
                sesh['fuel_lambda'].append(state.fuel.cmd_equivalence_ratio)
                sesh['speed'].append(state.speed)

            data.append(sesh)

        return data

    def get_summary(self):
        latest_state = (
            self.db_session.query(CarState)
                            .join(OBDSession, CarState.session_id == OBDSession.id)
                            .filter(OBDSession.user_id == self.user_id)
                            .order_by(CarState.id.desc())
                            .first()
        )
        speed_average = (
            self.db_session.query(func.avg(CarState.speed).label('speed_average'))
                            .join(OBDSession, CarState.session_id == OBDSession.id)
                            .filter(OBDSession.user_id == self.user_id)
                            .scalar()
        )
        rpm_average, load_average = (
            self.db_session.query(
                                func.avg(Engine.rpm).label('rpm_average'),
                                func.avg(Engine.load).label('load_average'),
                            )
                            .join(CarState, CarState.engine_id == Engine.id)
                            .join(OBDSession, CarState.session_id == OBDSession.id)
                            .filter(OBDSession.user_id == self.user_id)
                            .first()
        )

        data = {
            'fuel_level': latest_state.fuel.level if latest_state else None,
            'battery': {
                'latest': latest_state.voltage if latest_state else None,
                'threshold': BatteryLevel.MIN,
            },
            'speed_avg': speed_average,
            'engine': {
                'load_avg': load_average,
                'rpm_avg': rpm_average,
            }
        }
        return data

    def get_locations(self):
        sessions = (
            self.db_session.query(OBDSession)
                            .filter(OBDSession.user_id == self.user_id)
                            .order_by(OBDSession.date.asc())
                            .options(selectinload('car_states'))
        )

        items = []
        for session in sessions:
            sorted_car_states = sorted(session.car_states, key=lambda state: state.timestamp)
            items.append({
                'id': session.id,
                'date': session.date,
                'points': [car_state.gps.get_point() for car_state in sorted_car_states]
            })

        return items
