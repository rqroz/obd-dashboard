"""
Base ODB controllers.
"""
import datetime

from pandas import DataFrame

from app.controllers import BaseController
from app.constants.odb import CSV_COLUM_SENSOR_MAP, ODBSensorLabels
from app.models.odb.session import ODBSession


class BaseODBController(BaseController):
    """ Base ODB Controller """
    def _resolve_date_from_csv_row(self, csv_row: dict):
        """ Resolves a datetime from a certain row in a CSV """
        date_str = csv_row[CSV_COLUM_SENSOR_MAP[ODBSensorLabels.DATE]]
        return datetime.datetime.strptime(date_str[:-4], '%d-%b-%Y %H:%M:%S')


class BaseODBSensorController(BaseODBController):
    """ Base ODB Controller """
    def _register_values_csv(self,
                             db_model: any,
                             value_key: str,
                             session: ODBSession,
                             csv: DataFrame,
                             flush: bool = False):
        """
        Will read and store data related to the engine load from CSV for the current user.
        """
        for idx, row in csv.iterrows():
            try:
                eng_load = db_model(
                    session_id=session.id,
                    value=row[value_key],
                    date=self._resolve_date_from_csv_row(row),
                )
            except:
                continue

            self.db_session.add(eng_load)

        if flush:
            self.db_session.flush()
        else:
            self.db_session.commit()
