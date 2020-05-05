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
from app.models.odb.fuel import FuelLevel, FuelRatio
from app.models.user import User


class FuelController(BaseODBSensorController):
    """
    Controller class for Engine-related data manipulations.
    """
    def register_fuel_level_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the fuel level from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Fuel.LEVEL]
        self._register_values_csv(FuelLevel, value_key, session, csv, flush)

    def register_fuel_ratio_from_csv(self, session: ODBSession, csv: DataFrame, flush: bool = False):
        """
        Will read and store data related to the fuel ratio from CSV for the current user.
        """
        value_key = CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Fuel.RATIO]
        self._register_values_csv(FuelRatio, value_key, session, csv, flush)

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
