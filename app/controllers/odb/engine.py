"""
ODB Controller
"""
from pandas import DataFrame
from sqlalchemy.sql import func

from app.constants.odb import (
    ODBSensorLabels,
    CSV_COLUM_SENSOR_MAP,
)
from app.controllers.odb import BaseODBSensorController
from app.models.odb.session import ODBSession
from app.models.odb.engine import EngineLoad, EngineRPM
from app.models.user import User


class EngineControllerError(Exception):
    """ Exception class for EngineController """
    pass


class EngineController(BaseODBSensorController):
    """
    Controller class for Engine-related data manipulations.
    """
    def _get_average(self, engine_class: any, user: User):
        """
        Returns the average from the registered values for a certain Engine sensor,
        considering the complete history of a certain user.
        """
        return (
            self.db_session.query(func.avg(engine_class.value))
                            .filter(engine_class.session.has(user_id=user.id))
        ).scalar()

    def get_engine_load_avg(self, user: User):
        """
        Returns the average engine load considering the complete history of a certain user.
        """
        return self._get_average(EngineLoad, user)

    def get_engine_rpm_avg(self, user: User):
        """
        Returns the average engine RPM considering the complete history of a certain user.
        """
        return self._get_average(EngineRPM, user)

    def register_engine_load_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the engine load from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.LOAD]
        self._register_values_csv(EngineLoad, value_key, session, csv, flush)

    def register_engine_rpm_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the engine load from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Engine.RPM]
        self._register_values_csv(EngineRPM, value_key, session, csv, flush)