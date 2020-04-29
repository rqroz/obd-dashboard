"""
Engine-related OBD Readings.
"""
from app.database import DATABASE
from app.models.odb.abstract import ODBSensorValueMixin


class EngineLoad(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine Load data from ODB sensors. """
    __tablename__ = 'odb_engine_load'


class EngineRPM(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_rpm'


class Speed(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_speed'
