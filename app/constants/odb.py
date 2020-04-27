"""
ODB Specific constants.
"""

class ODBSensorPrefixes:
    FULL_NAME = 'userFullName'
    SHORT_NAME = 'userShortName'
    UNIT = 'userUnit'
    SENSOR = 'k'


class ODBSensorLabels:
    DATE = 'tmp'

    class GPS:
        LATITUDE = 'ff1006'
        LONGITUDE = 'ff1005'

    class Fuel:
        RATIO = 'ff1203' #KM/L

    class Engine:
        LOAD = 'tmp-eng-ld'


CSV_COLUM_SENSOR_MAP = {
    ODBSensorLabels.DATE: ' Device Time',
    ODBSensorLabels.GPS.LONGITUDE: ' Longitude',
    ODBSensorLabels.GPS.LATITUDE: ' Latitude',
    ODBSensorLabels.Engine.LOAD: 'Engine Load(Absolute)(%)',
}
