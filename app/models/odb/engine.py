"""
Engine-related OBD Readings.
"""
from app.constants.odb import ODBSensorLabels
from app.database import DATABASE
from app.models.odb.abstract import ODBSensorValueMixin


class EngineCoolantTemp(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_coolant_temp'

    SENSOR_KEY = ODBSensorLabels.Engine.COOLANT_TEMP


class EngineLoad(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine Load data from ODB sensors. """
    __tablename__ = 'odb_engine_load'

    SENSOR_KEY = ODBSensorLabels.Engine.LOAD


class EngineRPM(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_rpm'

    SENSOR_KEY = ODBSensorLabels.Engine.RPM


class EngineVoltage(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_voltage'

    SENSOR_KEY = ODBSensorLabels.Engine.VOLTAGE


class ManifoldPressure(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_map'

    SENSOR_KEY = ODBSensorLabels.Engine.MAP


class MassAirFlow(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_engine_maf'

    SENSOR_KEY = ODBSensorLabels.Engine.MAF


class Speed(DATABASE.Model, ODBSensorValueMixin):
    """ Readings for Engine RPM data from ODB sensors. """
    __tablename__ = 'odb_speed'

    SENSOR_KEY = ODBSensorLabels.Engine.SPEED
