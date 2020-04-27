"""
Fuel-related OBD Readings.
"""
from app.database import DATABASE
from app.models.odb.abstract import ODBSensorValueMixin


class FuelLevel(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Fuel Level data from ODB sensors. """
    __tablename__ = 'odb_fuel_level'
