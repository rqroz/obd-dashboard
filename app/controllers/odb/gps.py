"""
GPS Controller
"""
from sqlalchemy.orm import selectinload

from app.controllers.odb import BaseODBSensorController
from app.models.odb.session import ODBSession
from app.models.odb.gps import GPSReading
from app.models.user import User


class GPSController(BaseODBSensorController):
    """
    Controller class for GPS-related data manipulations.
    """
    MODEL_MAP = {
        'gps': GPSReading,
    }

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
