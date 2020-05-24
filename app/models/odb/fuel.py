"""
Fuel-related OBD Readings.
"""
from app.constants.odb import ODBSensorLabels
from app.database import DATABASE
from app.models.odb.abstract import ODBSensorValueMixin


class FuelLevel(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Fuel Level data from ODB sensors. """
    __tablename__ = 'odb_fuel_level'

    SENSOR_KEY = ODBSensorLabels.Fuel.LEVEL


class FuelRatio(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Fuel Ratio data from ODB sensors. """
    __tablename__ = 'odb_fuel_ratio'

    SENSOR_KEY = ODBSensorLabels.Fuel.RATIO


class FuelLambda(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_fuel_lambda'

    SENSOR_KEY = ODBSensorLabels.Fuel.LAMBDA
