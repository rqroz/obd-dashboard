"""
GPS Controller
"""
from sqlalchemy.orm import selectinload

from app.constants.odb import ODBSensorNames
from app.controllers.odb import BaseODBSensorController
from app.models.odb.session import ODBSession
from app.models.odb.gps import GPSReading
from app.models.user import User


class GPSController(BaseODBSensorController):
    """
    Controller class for GPS-related data manipulations.
    """
    MODEL_MAP = {
        ODBSensorNames.GPS.GPS: GPSReading,
    }

    def get_sensor_avg(self, user, sensor_key):
        """ We won't be implementing this method for GPS """
        raise NotImplementedError

    def get_sensor_latest_value(self, user):
        """
        Returns the latest read for GPS sensors attached to the current user.

        Args:
            - user (app.models.user.User): Currently authenticated user.

        Returns:
            - (dict): Map of lat and lng values.
        """
        model = list(self.MODEL_MAP.values())[0]
        latest = (
            self.db_session.query(model)
                            .filter(model.session.has(user_id=user.id))
                            .order_by(model.date.desc())
                            .first()
        )
        return latest.get_point() if latest else None

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
