"""
ODB Specific constants.
"""
class ODBSensorNames:
    class GPS:
        GPS = 'gps'

    class Fuel:
        LAMBDA = 'lambda'
        LEVEL = 'level'
        RATIO = 'ratio'

    class Engine:
        COOLANT_TEMP = 'coolant'
        LOAD = 'load'
        MAF = 'maf'
        MAP = 'map'
        RPM = 'rpm'
        SPEED = 'speed'
        VOLTAGE = 'battery'


class ODBSensorLabels:
    DATE = 'time'

    class GPS:
        LABEL = 'gps'
        LATITUDE = 'kff1006'
        LONGITUDE = 'kff1005'

    class Fuel:
        LAMBDA = 'k44'
        LEVEL = 'k2f'
        RATIO = 'kff1203'

    class Engine:
        COOLANT_TEMP = 'k5'
        LOAD = 'k43'
        MAF = 'k10'
        MAP = 'kb'
        RPM = 'kc'
        SPEED = 'kd'
        VOLTAGE = 'k42'


CSV_COLUM_SENSOR_MAP = {
    ODBSensorLabels.DATE: ' Device Time',

    ODBSensorLabels.GPS.LATITUDE: ' Latitude',
    ODBSensorLabels.GPS.LONGITUDE: ' Longitude',

    ODBSensorLabels.Engine.COOLANT_TEMP: 'Engine Coolant Temperature',
    ODBSensorLabels.Engine.LOAD: 'Engine Load(Absolute)(%)',
    ODBSensorLabels.Engine.MAF: 'Mass Air Flow Rate(g/s)',
    ODBSensorLabels.Engine.MAP: 'Intake Manifold Pressure(psi)',
    ODBSensorLabels.Engine.RPM: 'Engine RPM(rpm)',
    ODBSensorLabels.Engine.SPEED: 'Speed (OBD)(km/h)',
    ODBSensorLabels.Engine.VOLTAGE: 'Voltage (Control Module)(V)',

    ODBSensorLabels.Fuel.LEVEL: 'Fuel Level (From Engine ECU)(%)',
    ODBSensorLabels.Fuel.RATIO: 'Kilometers Per Litre(Instant)(kpl)',
    ODBSensorLabels.Fuel.LAMBDA: 'Commanded Equivalence Ratio(lambda)',
}


class BatteryLevel:
    MIN = 13.5
