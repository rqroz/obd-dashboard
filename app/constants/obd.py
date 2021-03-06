"""
OBD Specific constants.
"""
class CarSensorID:
    DATE = 'date'
    TIMESTAMP = 'time'

    SPEED = 'kd'
    VOLTAGE = 'k42'
    THROTTLE_POSITION = 'k11'

    class Accelerometer:
        TOTAL = 'kff1223'
        X = 'kff1220'
        Y = 'kff1221'
        Z = 'kff1222'

    class Engine:
        COOLANT_TEMP = 'k5'
        LOAD = 'k43'
        INTAKE_AIR_TEMP = 'kf'
        MAF = 'k10'
        MAP = 'kb'
        RPM = 'kc'

    class Fuel:
        LAMBDA = 'k44'
        LEVEL = 'k2f'
        RATIO = 'kff1203'
        USED = 'kff1271'

    class GPS:
        LATITUDE = 'kff1006'
        LONGITUDE = 'kff1005'


CSV_SENSOR_MAP = {
    CarSensorID.DATE: ' Device Time',
    CarSensorID.SPEED: 'Speed (OBD)(km/h)',
    CarSensorID.VOLTAGE: 'Voltage (Control Module)(V)',
    CarSensorID.THROTTLE_POSITION: 'Throttle Position(Manifold)(%)',

    CarSensorID.Accelerometer.TOTAL: 'Acceleration Sensor(Total)(g)',
    CarSensorID.Accelerometer.X: 'Acceleration Sensor(X axis)(g)',
    CarSensorID.Accelerometer.Y: 'Acceleration Sensor(Y axis)(g)',
    CarSensorID.Accelerometer.Z: 'Acceleration Sensor(Z axis)(g)',

    CarSensorID.Engine.COOLANT_TEMP: 'Engine Coolant Temperature',
    CarSensorID.Engine.LOAD: 'Engine Load(Absolute)(%)',
    CarSensorID.Engine.INTAKE_AIR_TEMP: 'Intake Air Temperature',
    CarSensorID.Engine.MAF: 'Mass Air Flow Rate(g/s)',
    CarSensorID.Engine.MAP: 'Intake Manifold Pressure(psi)',
    CarSensorID.Engine.RPM: 'Engine RPM(rpm)',

    CarSensorID.Fuel.LEVEL: 'Fuel Level (From Engine ECU)(%)',
    CarSensorID.Fuel.RATIO: 'Kilometers Per Litre(Instant)(kpl)',
    CarSensorID.Fuel.LAMBDA: 'Commanded Equivalence Ratio(lambda)',
    CarSensorID.Fuel.USED: 'Fuel used (trip)(l)',

    CarSensorID.GPS.LATITUDE: ' Latitude',
    CarSensorID.GPS.LONGITUDE: ' Longitude',
}


class BatteryLevel:
    MIN = 13.5
