"""
OBD Specific constants.
"""

class OBDSensorPrefixes:
    FULL_NAME = 'userFullName'
    SHORT_NAME = 'userShortName'
    UNIT = 'userUnit'
    SENSOR = 'k'


class OBDSensorLabels:
    DATE = 'tmp'

    class GPS:
        LATITUDE = 'ff1006'
        LONGITUDE = 'ff1005'

    class Fuel:
        RATIO = 'ff1203' #KM/L

    class Engine:
        LOAD = 'tmp-eng-ld'


CSV_COLUM_SENSOR_MAP = {
    OBDSensorLabels.DATE: ' Device Time',
    OBDSensorLabels.GPS.LONGITUDE: ' Longitude',
    OBDSensorLabels.GPS.LATITUDE: ' Latitude',
    OBDSensorLabels.Engine.LOAD: 'Engine Load(Absolute)(%)',
}
