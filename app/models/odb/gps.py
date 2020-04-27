"""
GPS OBD Readings.
"""
from sqlalchemy import Column, Numeric

from app.database import DATABASE
from app.models.odb.abstract import ODBSensorMixin


class GPSReading(DATABASE.Model, ODBSensorMixin):
    """ Readings for GPS data from ODB sensors. """
    __tablename__ = 'odb_gps_readings'

    lat = Column(Numeric, nullable=False)
    lng = Column(Numeric, nullable=False)

    def get_point(self):
        return {'lat': self.lat, 'lng': self.lng}
