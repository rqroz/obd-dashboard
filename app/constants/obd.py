"""
OBD Specific constants.
"""

class OBDSensorPrefixes:
    FULL_NAME = 'userFullName'
    SHORT_NAME = 'userShortName'
    UNIT = 'userUnit'
    SENSOR = 'k'


class OBDSensorLabels:
    class GPS:
        LATITUDE = 'ff1006'
        LONGITUDE = 'ff1005'

    class Fuel:
        RATIO = 'ff1203' #KM/L


CSV_COLUM_SENSOR_MAP = {
    ' Longitude': OBDSensorLabels.GPS.LONGITUDE,
    ' Latitude': OBDSensorLabels.GPS.LATITUDE,
}

CSV_DEVICE_TIME_COL = ' Device Time'
