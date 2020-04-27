"""
ODB Controller
"""
import pandas

from app.constants.odb import (
    ODBSensorLabels,
    CSV_COLUM_SENSOR_MAP,
)
from app.controllers.odb import BaseODBController
from app.models.odb.session import ODBSession
from app.models.odb.fuel import FuelLevel
from app.models.user import User


class FuelControllerError(Exception):
    """ Exception class for FuelController """
    pass


class FuelController(BaseODBController):
    """
    Controller class for Engine-related data manipulations.
    """
    def register_fuel_level_from_csv(self, session: ODBSession, csv: pandas.DataFrame, flush: bool = False):
        """
        Will read and store data related to the fuel level from CSV for the current user.
        """
        for idx, row in csv.iterrows():
            try:
                fuel_level = FuelLevel(
                    session_id=session.id,
                    value=row[CSV_COLUM_SENSOR_MAP[ODBSensorLabels.Fuel.LEVEL]],
                    date=self._resolve_date_from_csv_row(row),
                )
            except:
                continue

            self.db_session.add(fuel_level)

        if flush:
            self.db_session.flush()
        else:
            self.db_session.commit()

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
