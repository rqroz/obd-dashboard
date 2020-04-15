"""
OBD Specific constants.
"""

class OBDSensorPrefixes:
    FULL_NAME = 'userFullName'
    SHORT_NAME = 'userShortName'
    UNIT = 'userUnit'
    SENSOR = 'k'


class OBDSensorLabels:
    GPS_LATITUDE = 'ff1006'
    GPS_LONGITUDE = 'ff1005'
    FUEL_RATIO = 'ff1203' #KM/L
