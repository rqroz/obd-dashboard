"""
ODB Specific constants.
"""

class ODBSensorPrefixes:
    FULL_NAME = 'userFullName'
    SHORT_NAME = 'userShortName'
    UNIT = 'userUnit'
    SENSOR = 'k'


class ODBSensorLabels:
    DATE = 'time'

    class GPS:
        LATITUDE = 'kff1006'
        LONGITUDE = 'kff1005'

    class Fuel:
        RATIO = 'kff1203' #KM/L
        LEVEL = 'k2f'

    class Engine:
        LOAD = 'k43'
        RPM = 'k0c'
        SPEED = 'k0d'


CSV_COLUM_SENSOR_MAP = {
    ODBSensorLabels.DATE: ' Device Time',
    ODBSensorLabels.GPS.LONGITUDE: ' Longitude',
    ODBSensorLabels.GPS.LATITUDE: ' Latitude',
    ODBSensorLabels.Engine.LOAD: 'Engine Load(Absolute)(%)',
    ODBSensorLabels.Engine.RPM: 'Engine RPM(rpm)',
    ODBSensorLabels.Engine.SPEED: 'Speed (OBD)(km/h)',
    ODBSensorLabels.Fuel.LEVEL: 'Fuel Level (From Engine ECU)(%)',
}
