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
        RATIO = 'kff1203'
        LEVEL = 'k2f'

    class Engine:
        LOAD = 'k43'
        RPM = 'kc'
        SPEED = 'kd'


CSV_COLUM_SENSOR_MAP = {
    ODBSensorLabels.DATE: ' Device Time',
    ODBSensorLabels.GPS.LONGITUDE: ' Longitude',
    ODBSensorLabels.GPS.LATITUDE: ' Latitude',
    ODBSensorLabels.Engine.LOAD: 'Engine Load(Absolute)(%)',
    ODBSensorLabels.Engine.RPM: 'Engine RPM(rpm)',
    ODBSensorLabels.Engine.SPEED: 'Speed (OBD)(km/h)',
    ODBSensorLabels.Fuel.LEVEL: 'Fuel Level (From Engine ECU)(%)',
    ODBSensorLabels.Fuel.RATIO: 'Kilometers Per Litre(Instant)(kpl)',
}
