"""
ODB Controller
"""
import datetime

from decimal import Decimal
from pandas import DataFrame

from app.constants.odb import (
    ODBSensorLabels,
    CSV_COLUM_SENSOR_MAP,
)
from app.controllers.odb import BaseODBSensorController
from app.models.odb.session import ODBSession
from app.models.odb.fuel import (
    FuelLevel,
    FuelRatio,
    FuelLambda,
)
from app.models.user import User


class FuelController(BaseODBSensorController):
    """
    Controller class for Engine-related data manipulations.
    """
    def create_sensor_values_csv(self, session: ODBSession, csv: DataFrame):
        """
        Creates a list of fuel sensor instances from a TORQUE generated CSV.

        Args:
            - session (app.models.odb.session.ODBSession): Session to attach GPS reading instance;
            - csv (DataFrame): A dataframe representation of the TORQUE generated CSV.

        Returns:
            - (dict): A map of readings per sensor.
        """
        return {
            'lambda': FuelLambda.create_from_csv(session, csv),
            'level': FuelLevel.create_from_csv(session, csv),
            'ratio': FuelRatio.create_from_csv(session, csv),
        }

    def register_fuel_level(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save a FuelLevel record on the database.
        """
        return self._register_value(FuelLevel, session, value, date)

    def register_fuel_ratio(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save a FuelRatio record on the database.
        """
        return self._register_value(FuelRatio, session, value, date)

    def register_fuel_lambda(self, session: ODBSession, value: Decimal, date: datetime.datetime):
        """
        Will save a FuelLambda record on the database.
        """
        return self._register_value(FuelLambda, session, value, date)

    def get_latest_fuel_level(self, user: User):
        """ Get's the last fuel level value for the current user """
        level = (
            self.db_session.query(FuelLevel.value)
                            .filter(FuelLevel.session.has(user_id=user.id))
                            .order_by(FuelLevel.date.desc())
                            .first()
        )

        if level:
            return level.value
        return None
