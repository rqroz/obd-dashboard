"""
GPS OBD Readings.
"""
import datetime

from pandas import DataFrame
from sqlalchemy import Column, Numeric
from structlog import get_logger

from app.constants.odb import CSV_COLUM_SENSOR_MAP, ODBSensorLabels
from app.database import DATABASE
from app.models.odb.abstract import ODBSensorMixin
from app.models.odb.session import ODBSession


LOGGER = get_logger(__name__)


class GPSReading(DATABASE.Model, ODBSensorMixin):
    """ Readings for GPS data from ODB sensors. """
    __tablename__ = 'odb_gps_readings'

    SENSOR_LAT_KEY = ODBSensorLabels.GPS.LATITUDE
    SENSOR_LNG_KEY = ODBSensorLabels.GPS.LONGITUDE

    lat = Column(Numeric, nullable=False)
    lng = Column(Numeric, nullable=False)

    def get_point(self):
        return {'lat': self.lat, 'lng': self.lng}

    @classmethod
    def create_from_csv(cls, session: ODBSession, csv: DataFrame):
        """
        Will read and store data related to the engine load from CSV for the current user.
        """
        csv_lat_key = CSV_COLUM_SENSOR_MAP[cls.SENSOR_LAT_KEY]
        csv_lng_key = CSV_COLUM_SENSOR_MAP[cls.SENSOR_LNG_KEY]

        items = []
        for idx, row in csv.iterrows():
            try:
                item = cls(
                    session_id=session.id,
                    lat=row[csv_lat_key],
                    lng=row[csv_lng_key],
                    date=cls.resolve_date_from_csv_row(row),
                )
            except:
                continue

            items.append(item)

        return items

    @classmethod
    def create_from_torque(cls, session: ODBSession, request_data: dict, date: datetime.datetime):
        """
        Creates an instance from TORQUE's request data.

        Args:
            - session (app.models.odb.session.ODBSession): Current session to attach instance to;
            - request_data (dict): Request data from TORQUE.
            - date (datetime.datetime): Date to attach to instance.

        Returns:
            - (GPSReading | None): An instance of GPSReading, if able to resolve sensor data from the request.
                                   Otherwise, None.
        """
        if not (cls.SENSOR_LAT_KEY in request_data and cls.SENSOR_LNG_KEY in request_data):
            return None
        else:
            lat = request_data[cls.SENSOR_LAT_KEY]
            lng = request_data[cls.SENSOR_LNG_KEY]
            LOGGER.info(f'Will create instance of {cls.__name__}', value=f'({lat}, {lng})')
            return cls(session_id=session.id, lat=lat, lng=lng, date=date)
