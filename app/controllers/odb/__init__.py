"""
Base ODB controllers.
"""
import datetime

from app.controllers import BaseController
from app.constants.odb import CSV_COLUM_SENSOR_MAP, ODBSensorLabels


class BaseODBController(BaseController):
    """ Base ODB Controller """
    def _resolve_date_from_csv_row(self, csv_row: dict):
        """ Resolves a datetime from a certain row in a CSV """
        date_str = csv_row[CSV_COLUM_SENSOR_MAP[ODBSensorLabels.DATE]]
        return datetime.datetime.strptime(date_str[:-4], '%d-%b-%Y %H:%M:%S')
