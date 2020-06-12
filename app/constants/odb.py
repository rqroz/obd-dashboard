"""
ODB Specific constants.
"""
class CarSensorID:
    DATE = 'date'
    SPEED = 'kd'
    VOLTAGE = 'k42'

    class GPS:
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


CSV_SENSOR_MAP = {
    CarSensorID.DATE: ' Device Time',
    CarSensorID.SPEED: 'Speed (OBD)(km/h)',
    CarSensorID.VOLTAGE: 'Voltage (Control Module)(V)',

    CarSensorID.GPS.LATITUDE: ' Latitude',
    CarSensorID.GPS.LONGITUDE: ' Longitude',

    CarSensorID.Engine.COOLANT_TEMP: 'Engine Coolant Temperature',
    CarSensorID.Engine.LOAD: 'Engine Load(Absolute)(%)',
    CarSensorID.Engine.MAF: 'Mass Air Flow Rate(g/s)',
    CarSensorID.Engine.MAP: 'Intake Manifold Pressure(psi)',
    CarSensorID.Engine.RPM: 'Engine RPM(rpm)',

    CarSensorID.Fuel.LEVEL: 'Fuel Level (From Engine ECU)(%)',
    CarSensorID.Fuel.RATIO: 'Kilometers Per Litre(Instant)(kpl)',
    CarSensorID.Fuel.LAMBDA: 'Commanded Equivalence Ratio(lambda)',
}


class BatteryLevel:
    MIN = 13.5
