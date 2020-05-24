"""
ODB Controller
"""
import datetime

from pandas import DataFrame
from decimal import Decimal
from sqlalchemy.orm import selectinload

from app.constants.odb import (
    ODBSensorLabels,
    CSV_COLUM_SENSOR_MAP,
)
from app.controllers.odb import BaseODBController
from app.models.odb.session import ODBSession
from app.models.odb.gps import GPSReading
from app.models.user import User


class GPSController(BaseODBController):
    """
    Controller class for GPS-related data manipulations.
    """
    def create_sensor_values_csv(self, session: ODBSession, csv: DataFrame):
        """
        Creates a list of gps sensor instances from a TORQUE generated CSV.

        Args:
            - session (app.models.odb.session.ODBSession): Session to attach GPS reading instance;
            - csv (DataFrame): A dataframe representation of the TORQUE generated CSV.

        Returns:
            - (dict): A map of readings per sensor.
        """
        return {'gps': GPSReading.create_from_csv(session, csv)}

    def get_gps_readings(self, user: User):
        """
        Returns a list of GPS readings organized by session.

        Args:
            - user (app.models.user.User): User instance to be used when retrieving the sensor readings.

        Returns:
            (List[dict]): List of GPS points organized by session.
        """
        sessions = (
            self.db_session.query(ODBSession)
                            .filter(ODBSession.user_id == user.id)
                            .order_by(ODBSession.date.asc())
                            .options(selectinload('gps_readings'))
        )

        readings = []
        for session in sessions:
            readings.append({
                'session_id': session.id,
                'date': session.date,
                'points': [gps.get_point() for gps in session.gps_readings]
            })

        return readings

    def register_gps_reading(self, session: ODBSession, lat: Decimal, lng: Decimal, date: datetime.datetime):
        """
        Will save a GPSReading record on the database.

        Args:
            - session (app.models.odb.session.ODBSession): Session to be attached to new record.
            - lat (Decimal): Lattiude value.
            - lng (Decimal): Longitude value.
            - date (datetime.datetime): Date of reading.

        Returns:
            - gps_reading (app.models.odb.gps.GPSReading): An instance of the saved record on the database.
        """
        gps_reading = GPSReading(
            session_id=session.id,
            lat=lat,
            lng=lng,
            date=date
        )
        self.db_session.add(gps_reading)
        self.db_session.commit()
        return gps_reading
