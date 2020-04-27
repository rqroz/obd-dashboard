"""
Engine-related OBD Readings.
"""
from app.database import DATABASE
from app.models.odb.abstract import ODBSensorValueMixin


class EngineLoad(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine Load data from ODB sensors. """
    __tablename__ = 'odb_engine_load'
