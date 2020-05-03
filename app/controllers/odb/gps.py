"""
ODB Controller
"""
import pandas

from sqlalchemy.orm import selectinload

from app.constants.odb import (
    ODBSensorLabels,
    CSV_COLUM_SENSOR_MAP,
)
from app.controllers.odb import BaseODBController
from app.models.odb.session import ODBSession
from app.models.odb.gps import GPSReading
from app.models.user import User


class GPSControllerError(Exception):
    """ Exception class for GPSController Controller """
    pass


class GPSController(BaseODBController):
    """
    Controller class for GPS-related data manipulations.
    """
    def register_gps_from_csv(self, session: ODBSession, csv: pandas.DataFrame, flush: bool = False):
        """
        Will read gps data from a CSV and register the values for the current user.
        """
        values = csv[CSV_COLUM_SENSOR_MAP.values()]
        for idx, row in values.iterrows():
            try:
                reading = GPSReading(
                    session_id=session.id,
                    lat=row[CSV_COLUM_SENSOR_MAP[ODBSensorLabels.GPS.LATITUDE]],
                    lng=row[CSV_COLUM_SENSOR_MAP[ODBSensorLabels.GPS.LONGITUDE]],
                    date=self._resolve_date_from_csv_row(row)
                )
            except:
                continue

            self.db_session.add(reading)

        if flush:
            self.db_session.flush()
        else:
            self.db_session.commit()

    def get_gps_readings(self, user: User):
        """
        Returns a list of GPS readings organized by session.

        Args:
            - user (app.models.user.User): User instance to be used when retrieving the sensor readings.

        Returns:
            (List[dict]): List of GPS points organized by session.
        """
        db_data = (
            self.db_session.query(ODBSession)
                            .filter(ODBSession.user_id == user.id)
                            .order_by(ODBSession.date.asc())
                            .options(selectinload('gps_readings'))
        )

        readings = []
        for row in db_data:
            readings.append({
                'session_id': row.id,
                'date': row.date,
                'points': [gps.get_point() for gps in row.gps_readings]
            })

        return readings

    def register_gps_reading(self, session: ODBSession, lat, lng, date):
        gps_reading = GPSReading(
            session_id=session.id,
            lat=lat,
            lng=lng,
            date=date
        )
        self.db_session.add(gps_reading)
        self.db_session.commit()
        return gps_reading
