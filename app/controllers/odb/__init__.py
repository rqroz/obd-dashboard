"""
Base ODB controllers.
"""
import datetime

from decimal import Decimal
from pandas import DataFrame
from sqlalchemy.sql import func

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
    """ Base ODB Sensor Controller """
    MODEL_MAP = {} # To be overriden by subclasses

    def get_sensor_avg(self, user, sensor_key):
        """
        Returns the user's historical average (all sessions) for the sensor identified by <sensor_key> in <MODEL_MAP>.

        Args:
            - user (app.models.user.User): Currently authenticated user.

        Returns:
            - (decimal.Decimal): Historical average.
        """
        model = self.MODEL_MAP[sensor_key]
        return (
            self.db_session.query(func.avg(model.value))
                            .filter(model.session.has(user_id=user.id))
        ).scalar()

    def get_sensor_latest_value(self, user, sensor_key):
        """
        Returns the user's latest value for the sensor identified by <sensor_key> in <MODEL_MAP>.

        Args:
            - user (app.models.user.User): Currently authenticated user.

        Returns:
            - (dict): Map of lat and lng values.
        """
        model = self.MODEL_MAP[sensor_key]
        latest = (
            self.db_session.query(model.value)
                            .filter(model.session.has(user_id=user.id))
                            .order_by(model.date.desc())
                            .first()
        )
        return latest.value if latest else None

    def create_sensor_values_csv(self, session: ODBSession, csv: DataFrame):
        """
        Creates a list of sensor instances from a TORQUE generated CSV for each of the sensors in <MODEL_MAP>.

        Args:
            - session (app.models.odb.session.ODBSession): Session to attach GPS reading instance;
            - csv (DataFrame): A dataframe representation of the TORQUE generated CSV.

        Returns:
            - (dict): Map of readings per sensor.
        """
        return {key: model.create_from_csv(session, csv) for key, model in self.MODEL_MAP.items()}

    def create_sensor_values_torque(self, session: ODBSession, request_data: dict, date: datetime.datetime):
        """
        Creates an instance from each of the sensors in <MODEL_MAP>, based on TORQUE's request data.

        Args:
            - session (app.models.odb.session.ODBSession): Current session to attach instance to;
            - request_data (dict): Request data from TORQUE.
            - date (datetime.datetime): Date to attach to instance.

        Returns:
            - (dict): Map of instance per sensor.
        """
        return {key: model.create_from_torque(session, request_data, date) for key, model in self.MODEL_MAP.items()}
