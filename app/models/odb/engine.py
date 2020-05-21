"""
Engine-related OBD Readings.
"""
from app.database import DATABASE
from app.models.odb.abstract import ODBSensorValueMixin


class EngineCoolantTemp(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_coolant_temp'


class EngineLoad(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine Load data from ODB sensors. """
    __tablename__ = 'odb_engine_load'


class EngineRPM(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_rpm'


class EngineVoltage(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_voltage'


class ManifoldPressure(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_map'


class MassAirFlow(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_maf'


class Speed(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_speed'
